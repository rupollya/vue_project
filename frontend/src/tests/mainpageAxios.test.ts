import { beforeEach, test, describe, expect, vi } from 'vitest';
import axios from 'axios';
import mainpage from '@/components/Mainpage.vue';
import { shallowMount } from '@vue/test-utils';
import Cookies from 'js-cookie';

// Мокируем Bootstrap
global.bootstrap = {
  Modal: vi.fn(() => ({
    show: vi.fn(),
    hide: vi.fn(),
  })),
};

vi.mock('axios');

describe('Mainpage.vue', () => {
  beforeEach(() => {
    vi.resetAllMocks();
  });

  // Позитивные тесты
  test('Тест на успешное добавление задачи.', async () => {

    vi.spyOn(Cookies, 'get').mockReturnValue({ 'users_access_token': 'fake_token' });
    
    const token = Cookies.get('users_access_token');
    const wrapper = shallowMount(mainpage);
    const task = {
      task_id: 1,
      title: 'task',
      deadline: '10-10-2024',
      completed: false,
      importance: 'Низкая',
      user_id: 1,
      createdAt: new Date(),

    };

    await wrapper.vm.addTask(task);
    expect(axios.post).toHaveBeenCalledWith(`/api/task/create`, task, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      withCredentials: true
    });

  });

  test('Тест на успешное получение задач.', async () => {
    
    vi.spyOn(Cookies, 'get').mockReturnValue({ 'users_access_token': 'fake_token' });
    
    const token = Cookies.get('users_access_token');
    const wrapper = shallowMount(mainpage);

    const responseData = [
      {
        task_id: 1,
        title: 'task1',
        deadline: '10-10-2024',
        completed: false,
        importance: 'Низкая',
        user_id: 1,
        createdAt: new Date(),
      },
      {
        task_id: 2,
        title: 'task2',
        deadline: '11-10-2024',
        completed: true,
        importance: 'Высокая',
        user_id: 1,
        createdAt: new Date(),
      },
    ];

    vi.spyOn(axios, 'get').mockResolvedValue({ data: responseData });

    await wrapper.vm.fetchTasks();

    expect(axios.get).toHaveBeenCalledWith(`/api/task/user/task_all`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
      withCredentials: true,
    });

    expect(wrapper.vm.tasks).toEqual(responseData);
  });

  test('Тест на успешное удаление задачи.', async () => {
    
    vi.spyOn(Cookies, 'get').mockReturnValue({ 'users_access_token': 'fake_token' });
    
    const token = Cookies.get('users_access_token');
    const wrapper = shallowMount(mainpage);

    const taskId: string = '1'
    const task = {
      task_id: taskId,
      title: 'task',
      deadline: '10-10-2024',
      completed: false,
      importance: 'Низкая',
      user_id: 1,
      createdAt: new Date(),
    };

    vi.spyOn(axios, 'delete').mockResolvedValue({ data: {} });

    wrapper.vm.tasks = [task];

    await wrapper.vm.deleteTask(taskId);

    expect(axios.delete).toHaveBeenCalledWith(`/api/task/delete/${taskId}`, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      withCredentials: true,
    });

  });

  test('Тест на успешное изменение статуса задачи.', async () => {
    
    vi.spyOn(Cookies, 'get').mockReturnValue({ 'users_access_token': 'fake_token' });
    
    const token = Cookies.get('users_access_token');
    const wrapper = shallowMount(mainpage);

    const taskId: string = '1'
    const task = {
      task_id: taskId,
      title: 'task',
      deadline: '10-10-2024',
      completed: false,
      importance: 'Низкая',
      user_id: 1,
      createdAt: new Date(),
    };

    vi.spyOn(axios, 'put').mockResolvedValue({ data: {} });

    wrapper.vm.tasks = [task];

    await wrapper.vm.toggleTaskStatus(taskId);

    expect(axios.put).toHaveBeenCalledWith(`/api/task/${taskId}/update`, { completed: !task.completed }, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      withCredentials: true,
    });

  });

  test('Тест на успешное сохранение отредактированной задачи.', async () => {
    
    vi.spyOn(Cookies, 'get').mockReturnValue({ 'users_access_token': 'fake_token' });

    const token = Cookies.get('users_access_token');
    const wrapper = shallowMount(mainpage);

    const taskId: string = '1'
    const task = {
      task_id: taskId,
      title: 'task',
      deadline: '10-10-2024',
      completed: false,
      importance: 'Низкая',
      user_id: 1,
      createdAt: new Date(),
    };

    vi.spyOn(axios, 'put').mockResolvedValue({ data: {} });

    wrapper.vm.editedTask = task;
    wrapper.vm.tasks = [task];

    await wrapper.vm.saveEditedTask();

    expect(axios.put).toHaveBeenCalledWith(`/api/task/editing/${taskId}`, task, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      withCredentials: true,
    });
  });

  // Негативные тесты( с токеном пофиксить штучку)

  test('Тест на неуспешное изменение статуса задачи. Ошибка - произошла ошибка при изменение статуса', async () => {

    vi.spyOn(Cookies, 'get').mockReturnValue({ 'users_access_token': 'fake_token' });
    const token = Cookies.get('users_access_token');
    const wrapper = shallowMount(mainpage);

    const taskId: string = '1'
    const task = {
      task_id: taskId,
      title: 'task',
      deadline: '10-10-2024',
      completed: false,
      importance: 'Низкая',
      user_id: 1,
      createdAt: new Date(),
    };

    vi.spyOn(axios, 'put').mockRejectedValue(new Error());

    wrapper.vm.tasks = [task];
    const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => { })
    await wrapper.vm.toggleTaskStatus(taskId);

    expect(axios.put).toHaveBeenCalledWith(`/api/task/${taskId}/update`, { completed: !task.completed }, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      withCredentials: true,
    });
    expect(alertSpy).toHaveBeenCalledWith('Произошла ошибка при изменении статуса задачи. Попробуйте еще раз.');
  });

  test('Тест на неуспешное изменение статуса задачи. Ошибка - произошла ошибка при получении задачи.', async () => {

    vi.spyOn(Cookies, 'get').mockReturnValue({ 'users_access_token': 'fake_token' });
    const token = Cookies.get('users_access_token');
    const wrapper = shallowMount(mainpage);

    const taskId: string = '1'
    const task = {
      task_id: taskId,
      title: 'task',
      deadline: '10-10-2024',
      completed: false,
      importance: 'Низкая',
      user_id: 1,
      createdAt: new Date(),
    };

    vi.spyOn(axios, 'put').mockResolvedValue({ data: {} });

    wrapper.vm.tasks = [task];
    const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => { })
    await wrapper.vm.toggleTaskStatus(taskId);

    expect(axios.put).toHaveBeenCalledWith(`/api/task/${taskId}/update`, { completed: !task.completed }, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      withCredentials: true,
    });
    expect(alertSpy).toHaveBeenCalledWith('Произошла ошибка при получении задач. Попробуйте еще раз.');
  });

  test('Тест на другие ошибки при получении задач', async () => {
    vi.spyOn(Cookies, 'get').mockReturnValue({ 'users_access_token': 'fake_token' });
    const token = Cookies.get('users_access_token');
    const wrapper = shallowMount(mainpage);
    const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => { });

    await wrapper.vm.fetchTasks();

    expect(axios.get).toHaveBeenCalledWith(`/api/task/user/task_all`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
      withCredentials: true,
    });

    expect(alertSpy).toHaveBeenCalledWith('Произошла ошибка при получении задач. Попробуйте еще раз.');
  });

  test('Тест на неуспешное добавление задачи №1.', async () => {
    vi.spyOn(Cookies, 'get').mockReturnValue({ 'users_access_token': 'fake_token' });
    const token = Cookies.get('users_access_token');
    const wrapper = shallowMount(mainpage);
    const task = {
      task_id: 1,
      title: 'task',
      deadline: '10-10-2024',
      completed: false,
      importance: 'Низкая',
      user_id: 1,
      createdAt: new Date(),

    };
    const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => { });

    await wrapper.vm.addTask(task);

    expect(axios.post).toHaveBeenCalledWith(`/api/task/create`, task, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      withCredentials: true,
    });
    expect(alertSpy).toHaveBeenCalledWith('Произошла ошибка при получении задач. Попробуйте еще раз.');
  });

  test('Тест на неуспешное добавление задачи №2.', async () => {
    vi.spyOn(Cookies, 'get').mockReturnValue({ 'users_access_token': 'fake_token' });
    const token = Cookies.get('users_access_token');
    const wrapper = shallowMount(mainpage);
    const task = {
      task_id: 1,
      title: 'task',
      deadline: '10-10-2024',
      completed: false,
      importance: 'Низкая',
      user_id: 1,
      createdAt: new Date(),

    };
    const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => { });

    await wrapper.vm.addTask(task);

    expect(axios.post).toHaveBeenCalledWith(`/api/task/create`, task, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      withCredentials: true,
    });
    expect(alertSpy).toHaveBeenCalledWith('Произошла ошибка при добавлении задачи. Попробуйте еще раз.');
  });

  test('Тест на неуспешное удаление задачи №1.', async () => {
    vi.spyOn(Cookies, 'get').mockReturnValue({ 'users_access_token': 'fake_token' });
    const token = Cookies.get('users_access_token');
    const wrapper = shallowMount(mainpage);
    const taskId: string = '1'
    const task = {
      task_id: taskId,
      title: 'task',
      deadline: '10-10-2024',
      completed: false,
      importance: 'Низкая',
      user_id: 1,
      createdAt: new Date(),
    };

    vi.spyOn(axios, 'delete').mockResolvedValue({ data: {} });

    wrapper.vm.tasks = [task];
    const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => { });
    await wrapper.vm.deleteTask(taskId);

    expect(axios.delete).toHaveBeenCalledWith(`/api/task/delete/${taskId}`, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      withCredentials: true,
    });
    expect(alertSpy).toHaveBeenCalledWith('Произошла ошибка при получении задач. Попробуйте еще раз.');
  });

  test('Тест на неуспешное удаление задачи №2.', async () => {
    vi.spyOn(Cookies, 'get').mockReturnValue({ 'users_access_token': 'fake_token' });
    const token = Cookies.get('users_access_token');
    const wrapper = shallowMount(mainpage);
    const taskId: string = '1'
    const task = {
      task_id: taskId,
      title: 'task',
      deadline: '10-10-2024',
      completed: false,
      importance: 'Низкая',
      user_id: 1,
      createdAt: new Date(),
    };

    vi.spyOn(axios, 'delete').mockRejectedValue(new Error());

    wrapper.vm.tasks = [task];
    const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => { });
    await wrapper.vm.deleteTask(taskId);

    expect(axios.delete).toHaveBeenCalledWith(`/api/task/delete/${taskId}`, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      withCredentials: true,
    });
    expect(alertSpy).toHaveBeenCalledWith('Произошла ошибка при удалении задачи. Попробуйте еще раз.');
  });

  test('Тест на неуспешное редактирование задачи №1.', async () => {
    
    vi.spyOn(Cookies, 'get').mockReturnValue({ 'users_access_token': 'fake_token' });
    const token = Cookies.get('users_access_token');
    const wrapper = shallowMount(mainpage);

    const taskId: string = '1'
    const task = {
      task_id: taskId,
      title: 'task',
      deadline: '10-10-2024',
      completed: false,
      importance: 'Низкая',
      user_id: 1,
      createdAt: new Date(),
    };

    vi.spyOn(axios, 'put').mockRejectedValue(new Error());

    wrapper.vm.editedTask = task;
    wrapper.vm.tasks = [task];

    const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => { });

    await wrapper.vm.saveEditedTask();

    expect(axios.put).toHaveBeenCalledWith(`/api/task/editing/${taskId}`, task, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      withCredentials: true,
    });
    expect(alertSpy).toHaveBeenCalledWith('Произошла ошибка при редактировании задачи. Попробуйте еще раз.');
  });

  test('Тест на неуспешное редактирование задачи №2.', async () => {
    
    vi.spyOn(Cookies, 'get').mockReturnValue({ 'users_access_token': 'fake_token' });
    const token = Cookies.get('users_access_token');
    const wrapper = shallowMount(mainpage);

    const taskId: string = '1'
    const task = {
      task_id: taskId,
      title: 'task',
      deadline: '10-10-2024',
      completed: false,
      importance: 'Низкая',
      user_id: 1,
      createdAt: new Date(),
    };

    vi.spyOn(axios, 'put').mockResolvedValue({ data: {} });

    wrapper.vm.editedTask = task;
    wrapper.vm.tasks = [task];

    const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => { });

    await wrapper.vm.saveEditedTask();

    expect(axios.put).toHaveBeenCalledWith(`/api/task/editing/${taskId}`, task, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      withCredentials: true,
    });
    expect(alertSpy).toHaveBeenCalledWith('Произошла ошибка при получении задач. Попробуйте еще раз.');
  });
});