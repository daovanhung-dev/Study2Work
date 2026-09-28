abstract interface class SessionStore<T> {
  Future<T?> read();

  Future<void> save(T value);

  Future<void> clear();
}
