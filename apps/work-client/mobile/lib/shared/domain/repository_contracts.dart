abstract interface class JobRepository<TJob> {
  Future<List<TJob>> getAll();

  Future<TJob?> getById(int id);
}

abstract interface class CvRepository<TCv> {
  Future<TCv?> getById(int id);

  Future<bool> update(TCv cv);
}

abstract interface class CandidateRepository<TCandidate> {
  Future<List<TCandidate>> getAll();

  Future<void> updateStatus(int candidateId, String status);
}
