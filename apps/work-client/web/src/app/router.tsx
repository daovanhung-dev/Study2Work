import { Navigate, Route, Routes, useLocation } from "react-router-dom";
import type { ReactNode } from "react";

import { useAuth } from "../shared/auth/AuthProvider";
import { BusinessLayout, PublicLayout, StudentLayout } from "../layouts";
import { LoadingState } from "../shared/ui/States";
import {
  BusinessApplicationsPage,
  BusinessHomePage,
  BusinessJobFormPage,
  BusinessJobsPage,
  BusinessStaticPage,
  CvDetailPage,
  CvEditorPage,
  JobDetailPage,
  LogoutPage,
  StudentApplicationsPage,
  StudentHomePage,
  StudentStaticPage,
} from "../pages/WorkspacePages";
import {
  ComingSoonPage,
  BusinessRegisterPage,
  ErrorRolePage,
  HomePage,
  LoginPage,
  RegisterPage,
  RolePage,
} from "../pages/PublicPages";

export function canAccessRole(
  token: string | null,
  user: { role?: string } | null,
  role: "student" | "business",
): boolean {
  return Boolean(token && user && user.role === role);
}

function Protected({ role, children }: { role: "student" | "business"; children: ReactNode }) {
  const location = useLocation();
  const { token, user, hydrated } = useAuth();
  if (!hydrated) return <LoadingState />;
  if (!token) return <Navigate to={`/signInRole?returnTo=${encodeURIComponent(location.pathname)}`} replace />;
  if (!canAccessRole(token, user, role)) return <Navigate to="/errorRole" replace />;
  return <>{children}</>;
}

export function AppRouter() {
  return (
    <Routes>
      <Route element={<PublicLayout />}>
        <Route path="/" element={<HomePage />} />
        <Route path="/SignInStudent" element={<LoginPage role="student" />} />
        <Route path="/signInBusiness" element={<LoginPage role="business" />} />
        <Route path="/signInRole" element={<RolePage />} />
        <Route path="/signUpStudent" element={<RegisterPage />} />
        <Route path="/signUpBusiness" element={<BusinessRegisterPage />} />
        <Route path="/signUpRole" element={<RolePage register />} />
        <Route path="/coming-soon" element={<ComingSoonPage />} />
        <Route path="/errorRole" element={<ErrorRolePage />} />
      </Route>

      <Route element={<Protected role="student"><StudentLayout /></Protected>}>
        <Route path="/student/Home" element={<StudentHomePage />} />
        <Route path="/Student/Home" element={<StudentHomePage />} />
        <Route path="/student/JobDescription/:id" element={<JobDetailPage />} />
        <Route path="/Student/JobDescription/:id" element={<JobDetailPage />} />
        <Route path="/student/CV" element={<CvEditorPage />} />
        <Route path="/Student/CV" element={<CvEditorPage />} />
        <Route path="/student/CreateCV" element={<CvEditorPage />} />
        <Route path="/Student/CreateCV" element={<CvEditorPage />} />
        <Route path="/student/UpdateCV" element={<CvEditorPage />} />
        <Route path="/Student/UpdateCV" element={<CvEditorPage />} />
        <Route path="/student/Result" element={<StudentApplicationsPage />} />
        <Route path="/Student/Result" element={<StudentApplicationsPage />} />
        <Route path="/student/Logout" element={<LogoutPage />} />
        <Route path="/Student/Logout" element={<LogoutPage />} />
        <Route path="/student/:page" element={<StudentStaticPage />} />
        <Route path="/Student/:page" element={<StudentStaticPage />} />
      </Route>

      <Route element={<Protected role="business"><BusinessLayout /></Protected>}>
        <Route path="/business/Home" element={<BusinessHomePage />} />
        <Route path="/Business/Home" element={<BusinessHomePage />} />
        <Route path="/business/ManganerJD" element={<BusinessJobsPage />} />
        <Route path="/Business/ManganerJD" element={<BusinessJobsPage />} />
        <Route path="/business/PostJob" element={<BusinessJobFormPage />} />
        <Route path="/Business/PostJob" element={<BusinessJobFormPage />} />
        <Route path="/business/UpdateJD/:id" element={<BusinessJobFormPage />} />
        <Route path="/Business/UpdateJD/:id" element={<BusinessJobFormPage />} />
        <Route path="/business/ApplyList" element={<BusinessApplicationsPage />} />
        <Route path="/Business/ApplyList" element={<BusinessApplicationsPage />} />
        <Route path="/business/CVDetail/:id" element={<CvDetailPage />} />
        <Route path="/Business/CVDetail/:id" element={<CvDetailPage />} />
        <Route path="/business/Logout" element={<LogoutPage />} />
        <Route path="/Business/Logout" element={<LogoutPage />} />
        <Route path="/business/:page" element={<BusinessStaticPage />} />
        <Route path="/Business/:page" element={<BusinessStaticPage />} />
      </Route>

      <Route path="*" element={<Navigate to="/errorRole" replace />} />
    </Routes>
  );
}
