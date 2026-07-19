<script setup lang="ts">
import { studyApiBaseUrl } from "../shared/api/http";
</script>

<template>
  <main class="shell">
    <section class="hero">
      <p class="eyebrow">Study subsystem</p>
      <h1>Study2Work Study</h1>
      <p class="summary">
        Learning paths, lessons, assessment, progress, and verified evidence will live here.
      </p>
      <dl class="facts">
        <div>
          <dt>API</dt>
          <dd>{{ studyApiBaseUrl }}</dd>
        </div>
        <div>
          <dt>Health</dt>
          <dd>/health/live</dd>
        </div>
      </dl>
    </section>
  </main>
</template>
