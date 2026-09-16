(function () {
  "use strict";

  const TOKEN_KEY = "access_token";
  const originalFetch = window.fetch.bind(window);

  function getToken() {
    return window.localStorage.getItem(TOKEN_KEY);
  }

  function clearToken() {
    window.localStorage.removeItem(TOKEN_KEY);
  }

  function isSameOrigin(input) {
    const rawUrl = typeof input === "string" ? input : input.url;
    return new URL(rawUrl, window.location.href).origin === window.location.origin;
  }

  function withBearer(init) {
    const nextInit = init ? { ...init } : {};
    const headers = new Headers(nextInit.headers || {});
    const token = getToken();

    if (token && !headers.has("Authorization")) {
      headers.set("Authorization", `Bearer ${token}`);
    }

    nextInit.headers = headers;
    nextInit.credentials = "omit";
    return nextInit;
  }

  // Existing page-level fetch calls automatically become Bearer requests.
  window.fetch = function (input, init) {
    return originalFetch(input, isSameOrigin(input) ? withBearer(init) : init);
  };

  function showLoginError(message) {
    let errorBox = document.getElementById("jwt-login-error");
    if (!errorBox) {
      errorBox = document.createElement("div");
      errorBox.id = "jwt-login-error";
      errorBox.className = "alert alert-danger mb-3";
      const form = document.querySelector("[data-jwt-login]");
      form?.prepend(errorBox);
    }
    errorBox.textContent = message;
    errorBox.classList.remove("d-none");
  }

  function hideLoginError() {
    const errorBox = document.getElementById("jwt-login-error");
    errorBox?.classList.add("d-none");
  }

  function errorMessage(code) {
    if (code === "EMAIL_AND_PASSWORD_REQUIRED") {
      return "Email và mật khẩu bắt buộc.";
    }
    if (code === "INVALID_CREDENTIALS") {
      return "Email hoặc mật khẩu không đúng.";
    }
    return "Không thể đăng nhập. Vui lòng thử lại.";
  }

  async function login(form) {
    hideLoginError();
    const submitButton = form.querySelector("button[type=submit]");
    if (submitButton) submitButton.disabled = true;

    try {
      const response = await originalFetch(form.action, {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        },
        body: new URLSearchParams(new FormData(form)),
        credentials: "omit",
      });
      const data = await response.json().catch(() => ({}));

      if (!response.ok || typeof data.token !== "string") {
        showLoginError(errorMessage(data.error));
        return;
      }

      window.localStorage.setItem(TOKEN_KEY, data.token);
      await navigate(form.dataset.redirect || "/");
    } catch {
      showLoginError("Không thể kết nối máy chủ. Vui lòng thử lại.");
    } finally {
      if (submitButton) submitButton.disabled = false;
    }
  }

  function isLogoutUrl(url) {
    return /\/(student|business)\/logout$/i.test(url.pathname);
  }

  function logout() {
    clearToken();
    window.location.assign("/");
  }

  async function renderResponse(response, url, replace) {
    if (response.status === 401) {
      clearToken();
      window.location.assign("/signInRole");
      return;
    }
    if (response.status === 403) {
      window.location.assign("/errorRole");
      return;
    }
    if (!response.ok) {
      throw new Error(`Request failed with status ${response.status}`);
    }

    const contentType = response.headers.get("content-type") || "";
    if (!contentType.includes("text/html")) {
      const data = await response.json().catch(() => null);
      if (data?.message) window.alert(data.message);
      if (data?.redirect) await navigate(data.redirect);
      return data;
    }

    const html = await response.text();
    if (replace) {
      window.history.replaceState({}, "", url);
    } else {
      window.history.pushState({}, "", url);
    }
    document.open();
    document.write(html);
    document.close();
  }

  async function navigate(target, options) {
    const url = new URL(target, window.location.href);
    if (url.origin !== window.location.origin) {
      window.location.assign(url.href);
      return;
    }
    if (isLogoutUrl(url)) {
      logout();
      return;
    }
    if (!getToken() && /^\/(student|business)\//i.test(url.pathname)) {
      window.location.assign("/signInRole");
      return;
    }

    try {
      const response = await window.fetch(url.href, {
        headers: { Accept: "text/html" },
      });
      if (response.redirected && /\/signInRole$/i.test(new URL(response.url).pathname)) {
        clearToken();
        window.location.assign("/signInRole");
        return;
      }
      await renderResponse(response, url.pathname + url.search, options?.replace === true);
    } catch {
      window.location.assign(url.href);
    }
  }

  async function submit(form) {
    const method = (form.method || "GET").toUpperCase();
    const action = new URL(form.action || window.location.href, window.location.href);
    if (action.origin !== window.location.origin) return;

    if (method === "GET") {
      const query = new URLSearchParams(new FormData(form));
      action.search = query.toString();
      await navigate(action.href);
      return;
    }

    const response = await window.fetch(action.href, {
      method,
      body: new FormData(form),
      headers: { Accept: "text/html" },
    });
    if (response.redirected && /\/signInRole$/i.test(new URL(response.url).pathname)) {
      clearToken();
      window.location.assign("/signInRole");
      return;
    }
    await renderResponse(response, new URL(response.url).pathname, false);
  }

  window.s2wNavigate = navigate;
  window.s2wLogout = logout;
  window.s2wFetch = window.fetch;

  document.addEventListener("submit", function (event) {
    const form = event.target.closest("form");
    if (!form) return;

    if (form.matches("[data-jwt-login]")) {
      event.preventDefault();
      event.stopPropagation();
      void login(form);
      return;
    }

    const action = form.getAttribute("action");
    if (!action || action === "#" || action.startsWith("javascript:")) return;
    event.preventDefault();
    event.stopPropagation();
    void submit(form);
  }, true);

  document.addEventListener("click", function (event) {
    if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) {
      return;
    }

    const target = event.target.closest("a,button");
    if (!target) return;
    const href = target.getAttribute("href") || target.getAttribute("data-route");
    if (!href || href === "#" || href.startsWith("javascript:")) return;

    const url = new URL(href, window.location.href);
    if (url.origin !== window.location.origin) return;

    event.preventDefault();
    event.stopPropagation();
    void navigate(url.href);
  }, true);

  window.addEventListener("popstate", function () {
    void navigate(window.location.href, { replace: true });
  });
})();
