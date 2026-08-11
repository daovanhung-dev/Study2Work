import { useEffect, useState } from "react";

export function OfflineNotice() {
  const [online, setOnline] = useState(() =>
    typeof navigator === "undefined" ? true : navigator.onLine,
  );

  useEffect(() => {
    const markOnline = () => setOnline(true);
    const markOffline = () => setOnline(false);

    window.addEventListener("online", markOnline);
    window.addEventListener("offline", markOffline);

    return () => {
      window.removeEventListener("online", markOnline);
      window.removeEventListener("offline", markOffline);
    };
  }, []);

  if (online) {
    return null;
  }

  return (
    <div
      aria-live="assertive"
      className="border-b border-amber-300 bg-amber-50 px-4 py-3 text-center text-sm font-medium text-amber-950"
      role="status"
    >
      Bạn đang ngoại tuyến. Dữ liệu mới có thể chưa được tải; các thao tác quan trọng cần được thử lại
      khi có kết nối.
    </div>
  );
}
