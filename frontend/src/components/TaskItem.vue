<template>
  <div class="task mb-3 p-3 border rounded" :style="getTaskBackground(task.importance)">
    <h5 class="text-wrap">{{ task.title }}</h5>
    <p>Срок: {{ task.deadline || 'Дата не выбрана' }}</p>
    <p>Статус: {{ task.completed ? 'Завершена' : 'Не завершена' }}</p>
    <div class="d-flex  align-items-center">
      <button @click="toggleTaskStatus" class="btn btn-outline-light">
        {{ task.completed ? 'Отметить как незавершённую' : 'Отметить как завершённую' }}
      </button>
      <button @click="openEditModal()" class="btn btn-warning ms-2">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil" viewBox="0 0 16 16">
          <path d="M12.146.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1 0 .708l-10 10a.5.5 0 0 1-.168.11l-5 2a.5.5 0 0 1-.65-.65l2-5a.5.5 0 0 1 .11-.168l10-10zM11.207 2.5 13.5 4.793 14.793 3.5 12.5 1.207 11.207 2.5zm1.586 3L10.5 3.207 4 9.707V10h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.293l6.5-6.5zm-9.761 5.175-.106.106-1.528 3.821 3.821-1.528.106-.106A.5.5 0 0 1 5 12.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.468-.325z"/>
        </svg>
      </button>
      <button @click="deleteTask" class="btn btn-danger ms-2">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash-fill" viewBox="0 0 16 16">
          <path d="M2.5 1a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1H3v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V4h.5a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H10a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1H2.5zm3 4a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 .5-.5zM8 5a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7A.5.5 0 0 1 8 5zm3 .5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 1 0z"/>
        </svg>
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import { PropType } from 'vue';

interface Task {
  task_id: string;
  title: string;
  deadline: string | null;
  completed: boolean;
  importance: 'Низкая' | 'Средняя' | 'Высокая';
  user_id: number | null;
  createdAt: Date;
}

export default {
  props: {
    task: {
      type: Object as PropType<Task>,
      required: true,
    },
  },
  methods: {
    getTaskBackground(importance: 'Низкая' | 'Средняя' | 'Высокая') {
      switch (importance) {
        case 'Низкая':
          return { backgroundColor: '#79998A', borderRadius: '10px' };
        case 'Средняя':
          return { backgroundColor: 'rgba(255, 243, 205, 0.9)', borderRadius: '10px' };
        case 'Высокая':
          return { backgroundColor: '#C78376', borderRadius: '10px' };
        default:
          return { borderRadius: '10px' };
      }
    },
    toggleTaskStatus() {
    // console.log(this.task);  // Логируем перед эмитированием
    this.$emit('toggle-status', this.task.task_id);
    },
    deleteTask() {
      this.$emit('delete-task', this.task.task_id);
    },
    openEditModal() {
      this.$emit('edit-task', this.task.task_id);
    },
  },
};
</script>
<style>
.task{
  color:black;
}
</style>