<template>
  <div class="mt-4">
    <h4>Фильтры</h4>
    <!-- Кнопка для отображения всех задач -->
    <button 
      @click="filterTasks('all')" 
      class="btn btn-secondary mt-2 w-100 all-tasks">
      Все задачи
    </button>
    <!-- Кнопка для отображения завершенных задач -->
    <button 
      @click="filterTasks('completed')" 
      class="btn btn-secondary mt-2 w-100 completed-tasks">
      Завершенные
    </button>
    <!-- Кнопка для отображения незавершенных задач -->
    <button 
      @click="filterTasks('pending')" 
      class="btn btn-secondary mt-2 w-100 pending-tasks">
      Незавершенные
    </button>
  </div>
</template>


<script lang="ts">
import { defineComponent } from 'vue';

// Определение типов фильтров
type Filter = 'all' | 'completed' | 'pending';

export default defineComponent({
  methods: {
    // Метод для передачи выбранного фильтра родительскому компоненту
    filterTasks(filter: Filter) {
      this.$emit('filterTasks', filter);
    },
  },
});
</script>
