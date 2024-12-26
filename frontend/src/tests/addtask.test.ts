import { describe, test, expect, afterEach, beforeEach } from 'vitest';
import { shallowMount, VueWrapper } from '@vue/test-utils';
import AddTaskForm from '@/components/AddTaskForm.vue';

describe('AddTaskForm.vue', () => {

    let wrapper: VueWrapper<any> | null = null;
    beforeEach(() => {
        wrapper = shallowMount(AddTaskForm, {});
    })

    afterEach(() => {
        if (wrapper) {
            wrapper.unmount();
        }
    })
    
    // Положительные тесты
    test('Тест на добавление задачи с валидными данными.', () => {
        if (!wrapper) {
            throw new Error('wrapper не инициализирован');
        };

        wrapper.setData({
            newTask: {
                title: 'Новая задача',
                deadline: '2024-07-27',
                completed: false,
                importance: 'Средняя',
                user_id: null,
                createdAt: new Date(),
            },
        });

        wrapper.vm.addTask();
        expect(wrapper.emitted('add-task')).not.toBeNull();
    });

    test('Тест на сброс формы после добавления задачи.', () => {
        if (!wrapper) {
            throw new Error('wrapper не инициализирован');
        };

        wrapper.setData({
            newTask: {
                title: 'Новая задача',
                deadline: '2024-07-27',
                completed: false,
                importance: 'Средняя',
                user_id: null,
                createdAt: new Date(),
            },
        });

        wrapper.vm.addTask();
        expect(wrapper.vm.newTask.title).toBe('');
        expect(wrapper.vm.newTask.deadline).toBe('');
        expect(wrapper.vm.newTask.importance).toBe('Низкая');
    });

    // Отрицательные тесты
    test('Тест на добавление задачи с невалидными данными.', () => {

        if (!wrapper) {
            throw new Error('wrapper не инициализирован');
        };

        wrapper.setData({
            newTask: {
                title: '',
                deadline: '2024-07-27',
                completed: false,
                importance: 'Средняя',
                user_id: null,
                createdAt: new Date(),
            },
        });

        wrapper.vm.addTask();
        expect(wrapper.emitted('add-task')).toBeUndefined(); 
    });

})