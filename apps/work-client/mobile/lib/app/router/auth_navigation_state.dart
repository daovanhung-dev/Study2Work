import 'package:flutter/foundation.dart';

/// Runtime authentication state used by the app-level router.
///
/// The legacy login screens still own the current login behavior. They notify
/// this state only after the existing login/restore-session operation succeeds,
/// so go_router can enforce the auth boundary without changing that behavior.
class AuthNavigationState extends ChangeNotifier {
  AuthNavigationState._();

  static final AuthNavigationState instance = AuthNavigationState._();

  bool _isAuthenticated = false;

  bool get isAuthenticated => _isAuthenticated;

  void markAuthenticated() {
    if (_isAuthenticated) return;
    _isAuthenticated = true;
    notifyListeners();
  }

  void clear() {
    if (!_isAuthenticated) return;
    _isAuthenticated = false;
    notifyListeners();
  }
}
