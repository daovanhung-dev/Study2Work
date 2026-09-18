import { Prisma, PrismaClient } from "@prisma/client";
import request from "supertest";
import { afterEach, describe, expect, it } from "vitest";

import { createApp } from "../src/app.js";
import type { WorkConfig } from "../src/core/config.js";
import { signAccessToken } from "../src/core/security/access-token.js";
import type { WorkDependencies } from "../src/core/dependencies.js";

type Student = {
  id: bigint;
  hoten: string;
  email: string;
  matkhau: string;
  chuyennganh: string;
  avt: string | null;
};

type Business = {
  id: bigint;
  hoten: string;
  email: string;
  matkhau: string;
  diachi: string | null;
  sodienthoai: string | null;
  avt: string | null;
};

type Job = {
  id: bigint;
  ten_vi_tri: string;
  dia_diem: string | null;
  doanhnghiep_id: bigint | null;
  ten_cong_ty: string | null;
  ngay_tao: Date;
  [key: string]: unknown;
};

type Cv = {
  id: bigint;
  sinhvien_id: bigint;
  hoten: string;
  email: string;
  [key: string]: unknown;
};

type Application = {
  id: bigint;
  sinhvien_id: bigint;
  doanhnghiep_id: bigint;
  jd_id: bigint;
  created_at: Date;
  [key: string]: unknown;
};

type Store = {
  students: Student[];
  businesses: Business[];
  jobs: Job[];
  cvs: Cv[];
  applications: Application[];
  ready: boolean;
};

const config: WorkConfig = {
  appEnv: "test",
  port: 0,
  databaseUrl: "postgresql://test/test",
  directDatabaseUrl: "postgresql://test/test",
  jwtSecret: "test-secret-that-is-long-enough-for-work-api",
  jwtExpires: "1h",
  redisUrl: undefined,
  supabaseUrl: "",
  supabaseAnonKey: "",
};

function publicStudent(student: Student): Omit<Student, "matkhau"> {
  const { matkhau: _matkhau, ...data } = student;
  return data;
}

function publicBusiness(business: Business): Omit<Business, "matkhau"> {
  const { matkhau: _matkhau, ...data } = business;
  return data;
}

function createFakeDependencies(overrides: Partial<Store> = {}): { dependencies: WorkDependencies; store: Store } {
  const store: Store = {
    students: [{
      id: 1n,
      hoten: "Test Student",
      email: "student@example.com",
      matkhau: "legacy-password",
      chuyennganh: "IT",
      avt: null,
    }],
    businesses: [{
      id: 2n,
      hoten: "Test Business",
      email: "business@example.com",
      matkhau: "business-password",
      diachi: null,
      sodienthoai: null,
      avt: null,
    }],
    jobs: [{
      id: 10n,
      ten_vi_tri: "Backend Engineer",
      dia_diem: "Hanoi",
      doanhnghiep_id: 2n,
      ten_cong_ty: "Test Business",
      ngay_tao: new Date("2026-09-18T00:00:00.000Z"),
    }],
    cvs: [],
    applications: [],
    ready: true,
    ...overrides,
  };

  const prisma = {
    $connect: async () => undefined,
    $disconnect: async () => undefined,
    $queryRaw: async () => {
      if (!store.ready) throw new Error("database unavailable");
      return [{ result: 1 }];
    },
    $transaction: async <T>(callback: (transaction: typeof prisma) => Promise<T>) => callback(prisma),
    sinhVien: {
      findUnique: async ({ where, select }: { where: { id?: bigint; email?: string }; select?: Record<string, unknown> }) => {
        const student = store.students.find((item) =>
          where.id !== undefined ? item.id === where.id : item.email === where.email
        );
        if (!student) return null;
        return select?.matkhau ? { id: student.id, email: student.email, matkhau: student.matkhau } : publicStudent(student);
      },
      create: async ({ data }: { data: Omit<Student, "id"> }) => {
        if (store.students.some((item) => item.email === data.email)) {
          const error = new Prisma.PrismaClientKnownRequestError("duplicate", { code: "P2002", clientVersion: "test" });
          throw error;
        }
        const student = { ...data, id: BigInt(store.students.length + 1) };
        store.students.push(student);
        return publicStudent(student);
      },
      update: async ({ where, data }: { where: { id: bigint }; data: Partial<Student> }) => {
        const student = store.students.find((item) => item.id === where.id);
        if (!student) throw new Error("student missing");
        Object.assign(student, data);
        return publicStudent(student);
      },
    },
    doanhNghiep: {
      findUnique: async ({ where, select }: { where: { id?: bigint; email?: string }; select?: Record<string, unknown> }) => {
        const business = store.businesses.find((item) =>
          where.id !== undefined ? item.id === where.id : item.email === where.email
        );
        if (!business) return null;
        return select?.matkhau ? { id: business.id, email: business.email, matkhau: business.matkhau } : publicBusiness(business);
      },
      update: async ({ where, data }: { where: { id: bigint }; data: Partial<Business> }) => {
        const business = store.businesses.find((item) => item.id === where.id);
        if (!business) throw new Error("business missing");
        Object.assign(business, data);
        return publicBusiness(business);
      },
    },
    jD: {
      findMany: async ({ where }: { where?: { doanhnghiep_id?: bigint } } = {}) => store.jobs
        .filter((job) => !where?.doanhnghiep_id || job.doanhnghiep_id === where.doanhnghiep_id)
        .sort((left, right) => right.ngay_tao.getTime() - left.ngay_tao.getTime()),
      findUnique: async ({ where }: { where: { id: bigint } }) => store.jobs.find((job) => job.id === where.id) ?? null,
      findFirst: async ({ where }: { where: { id: bigint; doanhnghiep_id: bigint } }) => store.jobs.find((job) => job.id === where.id && job.doanhnghiep_id === where.doanhnghiep_id) ?? null,
      create: async ({ data }: { data: Record<string, unknown> }) => {
        const job = {
          ...data,
          id: BigInt(store.jobs.length + 11),
          ngay_tao: new Date("2026-09-19T00:00:00.000Z"),
        } as Job;
        store.jobs.push(job);
        return job;
      },
      update: async ({ where, data }: { where: { id: bigint }; data: Record<string, unknown> }) => {
        const job = store.jobs.find((item) => item.id === where.id);
        if (!job) throw new Error("job missing");
        Object.assign(job, data);
        return job;
      },
      delete: async ({ where }: { where: { id: bigint } }) => {
        const index = store.jobs.findIndex((job) => job.id === where.id);
        if (index < 0) throw new Error("job missing");
        return store.jobs.splice(index, 1)[0];
      },
    },
    cv: {
      count: async ({ where }: { where: { sinhvien_id: bigint } }) => store.cvs.filter((cv) => cv.sinhvien_id === where.sinhvien_id).length,
      findFirst: async ({ where }: { where: { id?: bigint; sinhvien_id: bigint } }) => store.cvs.find((cv) =>
        (where.id === undefined || cv.id === where.id) && cv.sinhvien_id === where.sinhvien_id
      ) ?? null,
      create: async ({ data }: { data: Record<string, unknown> }) => {
        const cv = { ...data, id: BigInt(store.cvs.length + 1) } as Cv;
        store.cvs.push(cv);
        return cv;
      },
      update: async ({ where, data }: { where: { id: bigint }; data: Record<string, unknown> }) => {
        const cv = store.cvs.find((item) => item.id === where.id);
        if (!cv) throw new Error("cv missing");
        Object.assign(cv, data);
        return cv;
      },
    },
    ungVien: {
      count: async ({ where }: { where: { sinhvien_id: bigint; doanhnghiep_id: bigint; jd_id: bigint } }) => store.applications.filter((item) =>
        item.sinhvien_id === where.sinhvien_id && item.doanhnghiep_id === where.doanhnghiep_id && item.jd_id === where.jd_id
      ).length,
      create: async ({ data }: { data: { sinhvien_id: bigint; doanhnghiep_id: bigint; jd_id: bigint } }) => {
        const application = { ...data, id: BigInt(store.applications.length + 1), created_at: new Date() };
        store.applications.push(application);
        return application;
      },
      findMany: async ({ where }: { where: { sinhvien_id?: bigint; doanhnghiep_id?: bigint } }) => store.applications.filter((item) =>
        (where.sinhvien_id === undefined || item.sinhvien_id === where.sinhvien_id) &&
        (where.doanhnghiep_id === undefined || item.doanhnghiep_id === where.doanhnghiep_id)
      ),
    },
  } as unknown as PrismaClient;

  return { dependencies: { config, prisma }, store };
}

function testApp(overrides: Partial<Store> = {}) {
  const { dependencies, store } = createFakeDependencies(overrides);
  return { app: createApp({ config, dependencies }), store };
}

afterEach(() => {
  // The app uses only injected dependencies; this keeps each test independent.
});

describe("Work system foundation", () => {
  it("returns the Work API root envelope", async () => {
    const { app } = testApp();
    const response = await request(app).get("/api/v1");

    expect(response.status).toBe(200);
    expect(response.body).toMatchObject({
      success: true,
      businessCode: "SYSTEM_ROOT_LOADED",
      message: "Welcome to Study2Work.",
      data: { service: "work-api" },
    });
    expect(response.headers["x-trace-id"]).toBe(response.body.traceId);
  });

  it("supports live/ready health and reports readiness failures", async () => {
    const healthy = testApp();
    const live = await request(healthy.app).get("/health/live");
    expect(live.status).toBe(200);
    expect(live.body.businessCode).toBe("SYSTEM_HEALTH_LIVE");
    expect(live.body.data).toEqual({ service: "work-api", environment: "test" });

    const ready = await request(healthy.app).get("/health/ready");
    expect(ready.status).toBe(200);
    expect(ready.body.businessCode).toBe("SYSTEM_HEALTH_READY");
    expect(ready.body.data.dependencies).toEqual({ database: "configured", redis: "not_configured" });

    const unhealthy = testApp({ ready: false });
    const failed = await request(unhealthy.app).get("/health/ready");
    expect(failed.status).toBe(503);
    expect(failed.body).toMatchObject({ success: false, businessCode: "DEPENDENCY_UNAVAILABLE", data: null });
  });

  it("accepts valid trace IDs and replaces invalid values", async () => {
    const { app } = testApp();
    const supplied = "7c3a2f1b-31c5-4a21-9b3e-7d1745c4748a";
    const accepted = await request(app).get("/health/live").set("X-Trace-Id", supplied);
    expect(accepted.body.traceId).toBe(supplied);
    expect(accepted.headers["x-trace-id"]).toBe(supplied);

    const replaced = await request(app).get("/health/live").set("X-Trace-Id", "invalid");
    expect(replaced.body.traceId).not.toBe("invalid");
    expect(replaced.body.traceId).toMatch(/^[0-9a-f-]{36}$/);
  });

  it("uses safe envelopes for unknown routes and malformed JSON", async () => {
    const { app } = testApp();
    const unknown = await request(app).get("/does-not-exist");
    expect(unknown.status).toBe(404);
    expect(unknown.body).toMatchObject({ success: false, businessCode: "NOT_FOUND", data: null });

    const malformed = await request(app)
      .post("/api/v1/auth/student/login")
      .set("Content-Type", "application/json")
      .send('{"email":');
    expect(malformed.status).toBe(400);
    expect(malformed.body).toMatchObject({ success: false, businessCode: "INVALID_REQUEST", data: null });
    expect(malformed.text).not.toContain("JWT_SECRET");
  });
});

describe("Work authentication and compatibility", () => {
  it("supports password and legacy matkhau login aliases with plaintext rehash", async () => {
    const { app, store } = testApp();
    const response = await request(app)
      .post("/api/v1/auth/student/login")
      .send({ email: "student@example.com", matkhau: "legacy-password" });

    expect(response.status).toBe(200);
    expect(response.body.businessCode).toBe("AUTH_LOGIN_SUCCESS");
    expect(response.body.data.user).toEqual({ id: 1, email: "student@example.com", role: "student" });
    expect(response.body.data.user).not.toHaveProperty("matkhau");
    expect(store.students[0].matkhau).toMatch(/^\$2[abxy]\$/);

    const invalid = await request(app)
      .post("/api/v1/auth/student/login")
      .send({ email: "student@example.com", password: "wrong" });
    expect(invalid.status).toBe(401);
    expect(invalid.body.businessCode).toBe("INVALID_CREDENTIALS");

    const missing = await request(app).post("/api/v1/auth/student/login").send({ email: "student@example.com" });
    expect(missing.status).toBe(400);
    expect(missing.body.meta.fieldErrors).toBeDefined();
  });

  it("keeps Bearer and role failures typed", async () => {
    const { app } = testApp();
    const missing = await request(app).post("/api/v1/auth/logout");
    expect(missing.status).toBe(401);
    expect(missing.body.businessCode).toBe("UNAUTHORIZED");

    const malformed = await request(app).get("/api/v1/me").set("Authorization", "Bearer not-a-token");
    expect(malformed.status).toBe(401);

    const businessToken = signAccessToken(config, { id: 2, email: "business@example.com", role: "business" });
    const forbidden = await request(app)
      .post("/api/v1/students/me/cv")
      .set("Authorization", `Bearer ${businessToken}`)
      .send({});
    expect(forbidden.status).toBe(403);
    expect(forbidden.body.businessCode).toBe("FORBIDDEN");
  });

  it("registers students without exposing password and rejects duplicate email", async () => {
    const { app } = testApp();
    const created = await request(app).post("/api/v1/students").send({
      hoten: "New Student",
      email: "new@example.com",
      matkhau: "new-password",
    });
    expect(created.status).toBe(201);
    expect(created.body.businessCode).toBe("STUDENT_CREATED");
    expect(created.body.data).not.toHaveProperty("matkhau");

    const duplicate = await request(app).post("/api/v1/students").send({
      hoten: "Duplicate",
      email: "student@example.com",
      matkhau: "another-password",
    });
    expect(duplicate.status).toBe(409);
    expect(duplicate.body.businessCode).toBe("STUDENT_CREATE_FAILED");
  });
});

describe("Work jobs and application boundary", () => {
  it("keeps jobs pagination and invalid/not-found ID behavior", async () => {
    const { app } = testApp();
    const page = await request(app).get("/api/v1/jobs?page=1&limit=1");
    expect(page.status).toBe(200);
    expect(page.body.businessCode).toBe("JOBS_LOADED");
    expect(page.body.meta).toEqual({ page: 1, limit: 1, total: 1, totalPages: 1 });
    expect(page.body.data[0].id).toBe(10);

    const invalid = await request(app).get("/api/v1/jobs/nope");
    expect(invalid.status).toBe(400);
    expect(invalid.body.businessCode).toBe("INVALID_REQUEST");

    const missing = await request(app).get("/api/v1/jobs/999");
    expect(missing.status).toBe(404);
    expect(missing.body.businessCode).toBe("JOB_NOT_FOUND");
  });

  it("creates an application and blocks a duplicate", async () => {
    const { app } = testApp();
    const token = signAccessToken(config, { id: 1, email: "student@example.com", role: "student" });
    const first = await request(app)
      .post("/api/v1/jobs/10/applications")
      .set("Authorization", `Bearer ${token}`);
    expect(first.status).toBe(201);
    expect(first.body.businessCode).toBe("APPLICATION_CREATED");

    const duplicate = await request(app)
      .post("/api/v1/jobs/10/applications")
      .set("Authorization", `Bearer ${token}`);
    expect(duplicate.status).toBe(409);
    expect(duplicate.body.businessCode).toBe("APPLICATION_ALREADY_EXISTS");

    const studentApplications = await request(app)
      .get("/api/v1/students/me/applications")
      .set("Authorization", `Bearer ${token}`);
    expect(studentApplications.status).toBe(200);
    expect(studentApplications.body.businessCode).toBe("APPLICATIONS_LOADED");

    const businessToken = signAccessToken(config, { id: 2, email: "business@example.com", role: "business" });
    const businessApplications = await request(app)
      .get("/api/v1/businesses/me/applications")
      .set("Authorization", `Bearer ${businessToken}`);
    expect(businessApplications.status).toBe(200);
    expect(businessApplications.body.businessCode).toBe("BUSINESS_APPLICATIONS_LOADED");
  });

  it("keeps CV ownership, duplicate protection and business applicant access", async () => {
    const { app } = testApp();
    const studentToken = signAccessToken(config, { id: 1, email: "student@example.com", role: "student" });
    const businessToken = signAccessToken(config, { id: 2, email: "business@example.com", role: "business" });

    const created = await request(app)
      .post("/api/v1/students/me/cv")
      .set("Authorization", `Bearer ${studentToken}`)
      .send({ hoten: "CV Student", email: "cv@example.com" });
    expect(created.status).toBe(201);
    expect(created.body.businessCode).toBe("CV_CREATED");
    expect(created.body.data.id).toBe(1);
    expect(created.body.data).not.toHaveProperty("matkhau");

    const duplicate = await request(app)
      .post("/api/v1/students/me/cv")
      .set("Authorization", `Bearer ${studentToken}`)
      .send({ hoten: "CV Duplicate", email: "duplicate@example.com" });
    expect(duplicate.status).toBe(409);
    expect(duplicate.body.businessCode).toBe("CV_ALREADY_EXISTS");

    const updated = await request(app)
      .put("/api/v1/students/me/cv/1")
      .set("Authorization", `Bearer ${studentToken}`)
      .send({ hoten: "CV Updated" });
    expect(updated.status).toBe(200);
    expect(updated.body.businessCode).toBe("CV_UPDATED");

    const applicantCv = await request(app)
      .get("/api/v1/students/1/cv")
      .set("Authorization", `Bearer ${businessToken}`);
    expect(applicantCv.status).toBe(200);
    expect(applicantCv.body.businessCode).toBe("CV_LOADED");
  });

  it("keeps business job ownership and CRUD behavior", async () => {
    const { app } = testApp();
    const businessToken = signAccessToken(config, { id: 2, email: "business@example.com", role: "business" });

    const created = await request(app)
      .post("/api/v1/businesses/me/jobs")
      .set("Authorization", `Bearer ${businessToken}`)
      .send({ ten_vi_tri: "Frontend Engineer", dia_diem: "Hanoi" });
    expect(created.status).toBe(201);
    expect(created.body.businessCode).toBe("JOB_CREATED");
    const jobId = created.body.data.id;

    const listed = await request(app)
      .get("/api/v1/businesses/me/jobs")
      .set("Authorization", `Bearer ${businessToken}`);
    expect(listed.status).toBe(200);
    expect(listed.body.businessCode).toBe("BUSINESS_JOBS_LOADED");

    const updated = await request(app)
      .put(`/api/v1/businesses/me/jobs/${jobId}`)
      .set("Authorization", `Bearer ${businessToken}`)
      .send({ dia_diem: "Ho Chi Minh City" });
    expect(updated.status).toBe(200);
    expect(updated.body.businessCode).toBe("JOB_UPDATED");

    const deleted = await request(app)
      .delete(`/api/v1/businesses/me/jobs/${jobId}`)
      .set("Authorization", `Bearer ${businessToken}`);
    expect(deleted.status).toBe(200);
    expect(deleted.body.businessCode).toBe("JOB_DELETED");
  });

  it("maps upload MIME and size violations through the central handler", async () => {
    const { app } = testApp();
    const invalidMime = await request(app)
      .post("/api/v1/students")
      .attach("avt", Buffer.from("not-an-image"), { filename: "avatar.txt", contentType: "text/plain" });
    expect(invalidMime.status).toBe(400);
    expect(invalidMime.body.businessCode).toBe("INVALID_REQUEST");

    const oversized = await request(app)
      .post("/api/v1/students")
      .attach("avt", Buffer.alloc(10 * 1024 * 1024 + 1, "x"), { filename: "avatar.png", contentType: "image/png" });
    expect(oversized.status).toBe(413);
    expect(oversized.body.businessCode).toBe("PAYLOAD_TOO_LARGE");
  });
});
