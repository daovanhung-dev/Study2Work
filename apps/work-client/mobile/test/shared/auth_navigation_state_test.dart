import 'package:flutter_test/flutter_test.dart';

import 'package:study2work_mobile/app/router/auth_navigation_state.dart';

void main() {
  test('notifies router listeners when authentication changes', () {
    final state = AuthNavigationState.instance;
    state.clear();

    var notifications = 0;
    void listener() => notifications++;
    state.addListener(listener);

    state.markAuthenticated();
    state.markAuthenticated();
    expect(state.isAuthenticated, isTrue);
    expect(notifications, 1);

    state.clear();
    expect(state.isAuthenticated, isFalse);
    expect(notifications, 2);

    state.removeListener(listener);
  });
}
