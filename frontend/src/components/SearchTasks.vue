<template>
    <div class="mt-3">
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
  
  interface Task {
    task_id: string;
    title: string;
    // другие поля задачи
  }
  
  export default {
    props: {
      tasks: {
        type: Array as PropType<Task[]>,
        required: true,
      },
    },
    data() {
      return {
        localSearchQuery: '',
      };
    },
    computed: {
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
      updateSearchQuery(event: Event): void {
        const target = event.target as HTMLInputElement;
        this.localSearchQuery = target.value;
        this.$emit('update-search', this.localSearchQuery);
      },
    },
  };
  </script>