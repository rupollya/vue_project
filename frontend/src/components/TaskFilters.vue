<template>
  <div class="mt-4">
    <h4>Фильтры</h4>
    <button @click="filterTasks('all')" class="btn btn-secondary mt-2 w-100">Все задачи</button>
    <button @click="filterTasks('completed')" class="btn btn-secondary mt-2 w-100">Завершенные</button>
    <button @click="filterTasks('pending')" class="btn btn-secondary mt-2 w-100">Незавершенные</button>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

type Filter = 'all' | 'completed' | 'pending';

export default defineComponent({
  methods: {
    filterTasks(filter: Filter) {
      this.$emit('filterTasks', filter);
    },
  },
});
</script>
