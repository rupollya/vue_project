<template>
  <form @submit.prevent="addTask">
    <h4>Добавление задачи</h4>
    <!-- Поле для ввода названия задачи -->
    <input id="nametask" v-model="newTask.title" type="text" placeholder="Название задачи" required class="form-control mb-2"
      maxlength="100" />
    <!-- Поле для выбора даты дедлайна -->
    <input id="date" v-model="newTask.deadline" type="date" class="form-control mb-2" />
    <!-- Секция выбора важности задачи -->
    <div class="d-flex justify-content-between align-items-center mb-2">
      <h5>Важность задачи</h5>
      <select v-model="newTask.importance" class="form-select w-auto">
        <option value="Низкая">Низкая</option>
        <option value="Средняя">Средняя</option>
        <option value="Высокая">Высокая</option>
      </select>
    </div>
    <!-- Кнопка для добавления задачи -->
    <button id="plus" type="submit" class="btn btn-secondary w-100">Добавить задачу</button>
  </form>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
// Структура задачи
interface Task {
  title: string;
  deadline: string;
  completed: boolean;
  importance: string;
  user_id: number | null;
  createdAt: Date;
}

const AddTaskForm = defineComponent({
  data(): { newTask: Task } {
    return {
      newTask: {
        title: '',
        deadline: '',
        completed: false,
        importance: 'Низкая',
        user_id: null,
        createdAt: new Date(),
      },
    };
  },
  methods: {
    // Метод для добавления новой задачи
    async addTask() {
      if (!this.newTask.title.trim()) {
        console.error('Название задачи не может быть пустым');
        return;
      }
      this.$emit('add-task', this.newTask);
      this.newTask = {
        title: '',
        deadline: '',
        completed: false,
        importance: 'Низкая',
        user_id: null,
        createdAt: new Date(),
      };
    },
  },
});
export default AddTaskForm;
</script>
