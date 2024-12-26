<template>
  <div class="mt-3">
    <!-- Поле для поиска задач -->
    <input 
      :value="localSearchQuery" 
      @input="updateSearchQuery" 
      type="text" 
      placeholder="Поиск задач..." 
      class="form-control mb-3"
    >
  </div>
</template>

<script lang="ts">
import { PropType } from 'vue';

// Интерфейс задачи
interface Task {
  task_id: string;
  title: string;
}

export default {
  props: {
    tasks: {
      type: Array as PropType<Task[]>, // Массив задач
      required: true,
    },
  },
  data() {
    return {
      localSearchQuery: '', // Локальная строка поиска
    };
  },
  computed: {
    // Фильтрация задач на основе строки поиска
    filteredTasks(): Task[] {
      if (!this.localSearchQuery) {
        return this.tasks;
      }
      return this.tasks.filter((task) =>
        task.title.toLowerCase().includes(this.localSearchQuery.toLowerCase())
      );
    },
  },
  methods: {
    // Обновление строки поиска
    updateSearchQuery(event: Event): void {
      const target = event.target as HTMLInputElement;
      this.localSearchQuery = target.value; // Устанавливаем значение локальной строки поиска
      this.$emit('update-search', this.localSearchQuery); // Эмитим событие для обновления строки поиска на родительском компоненте
    },
  },
};
</script>