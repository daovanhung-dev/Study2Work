import 'package:study2work_mobile/features/auth/domain/auth_repository.dart';
import 'package:study2work_mobile/features/business/legacy/controllers/cai_dat/cai_dat.dart'
    as session_controller;
import 'package:study2work_mobile/features/business/legacy/controllers/dang_nhap/dangnhap_ctrl.dart'
    as auth_controller;

final class BusinessAuthRepository implements AuthRepository {
  @override
  Future<bool> login(String email, String password) {
    return auth_controller.dangNhapDN(email, password);
  }

  @override
  Future<bool> restoreSession() async {
    return auth_controller.autoLogin();
  }

  @override
  Future<void> logout() {
    return session_controller.dangXuat();
  }
}
