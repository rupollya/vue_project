<template>
  <div>
    <!-- Навигационная панель -->
    <Navbar @exit-status="ExitStatus" />
    <div>
      <main class="container mt-4">
        <div class="row">
          <!-- Левая панель: добавление, поиск, фильтры -->
          <div class="col-4">
            <!-- Форма добавления задачи -->
            <AddTaskForm @add-task="addTask" />
            <!-- Поле поиска задач -->
            <SearchTask :search-query="searchQuery" :tasks="tasks" @update-search="updateSearch" />
            <!-- Фильтры задач -->
            <TaskFilters @filterTasks="filterTasks" />
            <!-- Кнопка открытия модального окна для выбора темы -->
            <button class="btn btn-light mt-5" @click="themeModal?.show()">
              Выбрать тему
            </button>
            <!-- Модальное окно для выбора темы -->
            <div class="modal fade" data-bs-keyboard="false" id="themeModal" tabindex="-1"
              aria-labelledby="themeModalLabel" aria-hidden="true">
              <div class="modal-dialog">
                <div class="modal-content">
                  <div class="modal-header">
                    <!-- Заголовок модального окна -->
                    <h5 class="modal-title" id="themeModalLabel">Выбор темы</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                  </div>
                  <div class="modal-body">
                    <!-- Кнопки выбора темы -->
                    <button class="btn w-100 mb-2" style="background-color: #e0dfde;"
                      @click="toggleTheme('light')">Светлая тема</button>
                    <button class="btn w-100 mb-2" style="background-color: #1a1f25;color: #e0dfde"
                      @click="toggleTheme('dark')">Темная тема</button>
                    <button class="btn w-100 mb-2" style="background-color: #3e5b5b"
                      @click="toggleTheme('green')">Зелёная тема</button>
                    <button class="btn w-100 mb-2" style="background-color: #a69892;"
                      @click="toggleTheme('blue')">Коричневая тема</button>
                    <button class="btn w-100 mb-2" style="background-color: #d8bcc6;"
                      @click="toggleTheme('pink')">Розовая тема</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <!-- Правая панель: список задач -->
          <div class="col-8">
            <!-- Заголовок и сортировка -->
            <div class="d-flex justify-content-between">
              <h3>
                <!-- Отображение текущего фильтра -->
                {{ currentFilter === 'all' ? 'Все задачи' : currentFilter === 'completed' ? 'Завершенные' :
                  'Незавершенные' }}
              </h3>
              <!-- Кнопки сортировки задач -->
              <div class="btn-group mb-2">
                <button @click="sortbynew" type="button" class="btn btn-outline-secondary" data-bs-toggle="tooltip"
                  title="Дальний срок">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                    class="bi bi-caret-down" viewBox="0 0 16 16">
                    <path
                      d="M3.204 5h9.4592L8 10.481 3.204 5zm-.753.659 4.796 5.48a1 1 0 0 0 1.506 0l4.796-5.48c.566-.647.106-1.659-.753-1.659H3.204a1 1 0 0 0-.753 1.659z" />
                  </svg>
                </button>
                <button @click="sortbyold" type="button" class="btn btn-outline-secondary" data-bs-toggle="tooltip"
                  title="Ближайший срок">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                    class="bi bi-caret-up" viewBox="0 0 16 16">
                    <path
                      d="M3.204 11h9.592L8 5.519 3.204 11zm-.753-.659 4.796-5.48a1 1 0 0 1 1.506 0l4.796 5.48c.566.647.106 1.659-.753 1.659H3.204a1 1 0 0 1-.753-1.659z" />
                  </svg>
                </button>
              </div>
            </div>
            <!-- Пустой список задач -->
            <div v-if="filteredTasks.length === 0" class="alert alert-info mt-2">Нет задач</div>
            <!-- Список задач -->
            <div v-else class="task-list" style="max-height: 600px; overflow-y: auto;">
              <!-- Компонент задачи -->
              <TaskItem v-for="task in filteredTasks" :key="task.task_id" :task="task" @toggle-status="toggleTaskStatus"
                @delete-task="deleteTask" @edit-task="openEditModal" />
            </div>
          </div>
        </div>
      </main>
    </div>

    <!-- Модальное окно редактирования задачи -->
    <div class="modal fade" id="editTaskModal" tabindex="-1" aria-labelledby="editTaskModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <!-- Заголовок окна редактирования -->
            <h5 class="modal-title" id="editTaskModalLabel">Редактировать задачу</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <!-- Поля редактирования задачи -->
            <input v-model="editedTask.title" type="text" class="form-control" placeholder="Название задачи" required
              ref="titleInput" @input="removeInvalidClass">
            <input v-model="editedTask.deadline" type="date" class="form-control mt-2" placeholder="Дата выполнения">
            <div class="d-flex justify-content-between align-items-center mt-2">
              <h5>Важность задачи</h5>
              <select v-model="editedTask.importance" class="form-select w-auto">
                <option value="Низкая">Низкая</option>
                <option value="Средняя">Средняя</option>
                <option value="Высокая">Высокая</option>
              </select>
            </div>
          </div>
          <div class="modal-footer">
            <!-- Кнопки управления -->
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
            <button type="button" class="btn btn-primary" @click="saveEditedTask">Сохранить изменения</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import AddTaskForm from './AddTaskForm.vue';
import Navbar from './navbarmain.vue';
import TaskItem from './TaskItem.vue';
import TaskFilters from './TaskFilters.vue';
import SearchTask from './SearchTasks.vue';
import Cookies from 'js-cookie';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Modal } from 'bootstrap';
import 'bootstrap'

// Тип для фильтров задач
type Filter = 'all' | 'completed' | 'pending';

// Интерфейс для задачи
interface Task {
  task_id: string; // Уникальный идентификатор задачи
  title: string; // Название задачи
  deadline: string; // Дата выполнения задачи
  completed: boolean; // Статус выполнения задачи
  importance: 'Низкая' | 'Средняя' | 'Высокая'; // Важность задачи
  user_id: number; // Идентификатор пользователя
  createdAt: Date; // Дата создания задачи
}

export default defineComponent({
  components: {
    AddTaskForm,
    Navbar,
    TaskItem,
    TaskFilters,
    SearchTask
  },
  data() {
    return {
      tasks: [] as Task[], // Массив задач
      currentFilter: 'all' as Filter, // Текущий фильтр задач (по умолчанию 'all')
      editedTask: { title: '', deadline: '', id: null, importance: '' } as unknown as Task, // Данные редактируемой задачи
      searchQuery: '', // Строка для поиска задач
      isDarkTheme: true, // Флаг для переключения между светлой и темной темой
      themeModal: null as Modal | null, // Модальное окно для выбора темы
    };
  },
  mounted() {
    // Инициализация модального окна для темы
    this.themeModal = new bootstrap.Modal(document.getElementById('themeModal'));

    // Загрузка сохраненной темы из localStorage
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
      this.isDarkTheme = savedTheme === 'dark'; // Установка флага темы
      this.applyTheme(savedTheme); // Применение сохраненной темы
    } else {
      this.applyTheme('dark'); // Установка темы по умолчанию
    }

    // Повторная инициализация модального окна, если оно уже было создано
    this.themeModal = new bootstrap.Modal(document.getElementById('themeModal'));

  },
  computed: {
    // Фильтр задач на основе текущего фильтра и строки поиска
    filteredTasks(): Task[] {
      if (this.currentFilter === 'completed') {
        // Завершенные задачи
        return this.tasks.filter((task: {
          title: any; completed: any;
        }) => task.completed && task.title.toLowerCase().includes(this.searchQuery.toLowerCase()));
      } else if (this.currentFilter === 'pending') {
        // Незавершенные задачи
        return this.tasks.filter((task: {
          title: any; completed: any;
        }) => !task.completed && task.title.toLowerCase().includes(this.searchQuery.toLowerCase()));
      }
      // Все задачи (по умолчанию)
      return this.tasks.filter((task: { title: any; }) => task.title.toLowerCase().includes(this.searchQuery.toLowerCase())); // Для 'all' возвращаем все задачи текущего пользователя
    },
  },
  created() {
    // Загрузка задач при создании компонента
    this.fetchTasks();
  },
  methods: {
    // Переключение темы
    toggleTheme(theme: string) {
      localStorage.setItem('theme', theme); // Сохранение темы в localStorage
      this.applyTheme(theme); // Применение выбранной темы
      this.themeModal?.hide(); // Закрытие модального окна
    },
    // Применение темы
    applyTheme(theme: string) {
      document.body.className = `theme-${theme}`;
    },
    // Обновление строки поиска
    updateSearch(query: string) {
      this.searchQuery = query;
    },
    // Получение задач
    async fetchTasks() {
      const token = Cookies.get('users_access_token'); // Получение токена пользователя из cookies
      try {
        const response = await axios.get('/api/task/user/task_all', {
          headers: {
            'Authorization': `Bearer ${token}`, // Авторизация через Bearer токен
          },
          withCredentials: true // Использование cookies в запросах
        });
        this.tasks = response.data; // Задачи возвращаются сервером и сохраняются в массив tasks
      }
      catch (error: any) {
        // Обработка ошибок, связанных с запросом
        if (axios.isAxiosError(error)) {
          if (error.response && error.response.status === 401) {
            alert('Ошибка аутентификации'); // Ошибка авторизации
          }
        } else {
          console.error(error); // Вывод ошибки в консоль
          alert('Произошла ошибка при получении задач. Попробуйте еще раз.');
        }
      }
    },
    // Добавление новой задачи
    async addTask(task: Task) {
      const token = Cookies.get('users_access_token'); // Получение токена пользователя
      try {
        const response = await axios.post('/api/task/create', task, {
          headers: {
            'Content-Type': 'application/json', // Указание типа контента
            'Authorization': `Bearer ${token}`, // Авторизация через Bearer токен
          },
          withCredentials: true, // Использование cookies в запросах
        });
        console.log('Добавленная задача:', response.data); // Логируем добавленную задачу
        this.tasks.push(response.data); // Добавляем задачу в список
      } catch (error: any) {
        // Обработка ошибок
        if (axios.isAxiosError(error)) {
          if (error.response && error.response.status === 401) {
            console.error('Ошибка аутентификации'); // Ошибка авторизации
          }
        } else {
          console.error('Ошибка при добавлении задачи:', error);
          alert('Произошла ошибка при добавлении задачи. Попробуйте еще раз.');
        }
      }
    },
    // Сортировка по новому времени создания (по убыванию)
    sortbynew() {
      this.tasks.sort((a: Task, b: Task) => {
        const dateA = a.createdAt instanceof Date ? a.createdAt.getTime() : new Date(a.createdAt).getTime();
        const dateB = b.createdAt instanceof Date ? b.createdAt.getTime() : new Date(b.createdAt).getTime();
        return dateB - dateA; // Сортировка по убыванию
      });
    },
    // Сортировка по старому времени создания (по возрастанию)
    sortbyold() {
      this.tasks.sort((a: Task, b: Task) => {
        const dateA = a.createdAt instanceof Date ? a.createdAt.getTime() : new Date(a.createdAt).getTime();
        const dateB = b.createdAt instanceof Date ? b.createdAt.getTime() : new Date(b.createdAt).getTime();
        return dateA - dateB; // сортировка по возрастанию
      });
    },
    // Изменение статуса задачи (завершена/незавершена)
    async toggleTaskStatus(taskId: string) {
      const token = Cookies.get('users_access_token');
      console.log('Token:', token);
      console.log("Идентификатор задачи:", taskId);
      // Поиск задачи по идентификатору
      const task = this.tasks.find((task: { task_id: string; }) => task.task_id === taskId);
      if (task) {
        try {
          console.log(taskId);
          const response = await axios.put(`/api/task/${taskId}/update`, { completed: !task.completed }, {
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`,
            },
            withCredentials: true,
          });
          task.completed = response.data.completed;
        }
        catch (error: any) {
          if (axios.isAxiosError(error)) {
            if (error.response && error.response.status === 401) {
              console.error('Ошибка аутентификации');
            }
          }
          else {
            console.error('Ошибка при изменении статуса задачи:', error);
            alert('Произошла ошибка при изменении статуса задачи. Попробуйте еще раз.');
          }
        }
      }
    },
    // Удаление задачи
    async deleteTask(taskId: string) {
      const token = Cookies.get('users_access_token');
      console.log('Token:', token);
      // Поиск задачи по идентификатору
      const task = this.tasks.find((task: { task_id: string; }) => task.task_id === taskId);
      if (task) {
        try {
          console.log(taskId);
          const response = await axios.delete(`/api/task/delete/${taskId}`, {
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`,
            },
            withCredentials: true,
          });
          await this.fetchTasks();
          console.log(response);
        }
        catch (error: any) {
          if (axios.isAxiosError(error)) {
            if (error.response && error.response.status === 401) {
              console.error('Ошибка аутентификации');
            }
          }
          else {
            console.error('Ошибка при изменении удалении задачи:', error);
            alert('Произошла ошибка при удалении задачи. Попробуйте еще раз.');
          }
        }
      }
    },
    // Открытие модального окна для редактирования задачи
    async openEditModal(taskId: string) {
      const task = this.tasks.find(task => task.task_id === taskId);
      if (task) {
        this.editedTask = { ...task };
        const modal = new bootstrap.Modal(document.getElementById('editTaskModal'));
        modal.show();
      }
    },
    // Сохранение изменений в задаче
    async saveEditedTask() {
      const token = Cookies.get('users_access_token');
      if (!this.editedTask.title.trim()) {
        this.$nextTick(() => {
          (this.$refs.titleInput as HTMLInputElement).classList.add('is-invalid');
        });
        return;
      }
      try {
        const response = await axios.put(`/api/task/editing/${this.editedTask.task_id}`, this.editedTask, {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
          withCredentials: true,
        });
        console.log(response);

        const modal = bootstrap.Modal.getInstance(document.getElementById('editTaskModal'));
        modal.hide();
        // Вызов функции для получения задач
        await this.fetchTasks();
      }
      catch (error: any) {
        if (axios.isAxiosError(error)) {
          if (error.response && error.response.status === 401) {
            console.error('Ошибка аутентификации');
          }
        }
        else {
          alert('Произошла ошибка при редактировании задачи. Попробуйте еще раз.');
        }
      }
    },
    // Удаление класса ошибки при вводе
    removeInvalidClass() {
      (this.$refs.titleInput as HTMLInputElement).classList.remove('is-invalid');
    },
    // Изменение фильтра задач
    filterTasks(filter: Filter) {
      this.currentFilter = filter;
    },
    // Выход из системы (удаление токена и перезагрузка страницы)
    ExitStatus() {
      Cookies.remove('users_access_token');
      this.$router.push('/').then(() => {
        this.$router.go(0); // Обновляем страницу после перехода (для сброса стилей)
      });
    },

  },
});
</script>
