import { describe, test, expect, afterEach, beforeEach } from 'vitest';
import { shallowMount, VueWrapper } from '@vue/test-utils';
import taskitem from '@/components/TaskItem.vue';


describe('TaskItem.vue', () => {

    let wrapper: VueWrapper<any> | null = null;
    
    let task = {
        task_id: '1',
        title: 'Тестовая задача',
        deadline: null,
        completed: false,
        importance: 'Низкая',
        user_id: null,
        createdAt: new Date(),
    };

    beforeEach(() => {
        wrapper = shallowMount(taskitem, {
            props: {
                task: task,
            },
        });
    });

    afterEach(() => {
        if (wrapper) {
            wrapper.unmount();
        }
    });

    test('Тест на проверку getTaskBackground возвращает правильные стили в зависимости от заданного importance', () => {
        
        if (!wrapper) {
            throw new Error('wrapper не инициализирован');
        }
        expect(wrapper.vm.getTaskBackground('Низкая')).toEqual({ backgroundColor: '#79998A', borderRadius: '10px', });

        expect(wrapper.vm.getTaskBackground('Средняя')).toEqual({ backgroundColor: 'rgba(255, 243, 205, 0.9)', borderRadius: '10px', });

        expect(wrapper.vm.getTaskBackground('Высокая')).toEqual({ backgroundColor: '#C78376', borderRadius: '10px', });
    });

    test('Тест эмитирования события toggle-status с правильным task_id при вызове toggleTaskStatus',  () => {

        if (!wrapper) {
            throw new Error('wrapper не инициализирован');
        }
        wrapper.vm.toggleTaskStatus();
        expect(wrapper.emitted('toggle-status')).toBeTruthy();
        expect(wrapper.emitted('toggle-status')?.[0]).toEqual([task.task_id]);
    });

    test('Тест эмитирования события delete-task с правильным task_id при вызове deleteTask',  () => {

        if (!wrapper) {
            throw new Error('wrapper не инициализирован');
        }
        wrapper.vm.deleteTask();
        expect(wrapper.emitted('delete-task')).toBeTruthy();
        expect(wrapper.emitted('delete-task')?.[0]).toEqual([task.task_id]);
    });

    test('Тест эмитирования события edit-task с правильным task_id при вызове openEditModal',  () => {

        if (!wrapper) {
            throw new Error('wrapper не инициализирован');
        }

        wrapper.vm.openEditModal();
        expect(wrapper.emitted('edit-task')).toBeTruthy();
        expect(wrapper.emitted('edit-task')?.[0]).toEqual([task.task_id]);
    });



});

