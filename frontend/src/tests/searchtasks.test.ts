import { describe, test, expect, afterEach, beforeEach } from 'vitest';
import { shallowMount, VueWrapper } from '@vue/test-utils';
import searchtasks from '@/components/SearchTasks.vue';

describe('SearchTasks.vue', () => {

    let wrapper: VueWrapper<any> | null = null;
    beforeEach(() => {
        wrapper = shallowMount(searchtasks, {});
    })

    afterEach(() => {
        if (wrapper) {
            wrapper.unmount();
        }
    })

    // положительные тесты

    test('Тест на функциональность поиска с корректным вводом', async () => {

        if (!wrapper) {
            throw new Error('wrapper не инициализирован');
        }

        const tasks = [
            { task_id: '1', title: 'Задача 1' },
            { task_id: '2', title: 'Задача 2' },
            { task_id: '3', title: 'Задача 3' },
        ];

        wrapper.setProps({ tasks });

        // пишем в поиск задача 2
        await wrapper.find('input').setValue('задача 2');

        // проверяем, что вычисляемое свойство filteredTasks возвращает правильный результат
        expect(wrapper.vm.filteredTasks).toEqual([{ task_id: '2', title: 'Задача 2' }]);

        // проверяем, что событие 'update-search' отправляется с правильным значением
        const emits = wrapper.emitted();
        expect(emits['update-search']).toEqual([['задача 2']]);
    });

    test('Тест на пустой поисковый запрос', async () => {
        if (!wrapper) {
            throw new Error('wrapper не инициализирован');
        }

        const tasks = [
            { task_id: '1', title: 'Задача 1' },
            { task_id: '2', title: 'Задача 2' },
            { task_id: '3', title: 'Задача 3' },
        ];

        wrapper.setProps({ tasks });
        await wrapper.find('input').setValue('');

        expect(wrapper.vm.filteredTasks).toEqual(tasks);
    });

    test('Тест на возврат пустого массива, при поиске несуществующей задачи', async () => {
        if (!wrapper) {
            throw new Error('wrapper не инициализирован');
        }

        const tasks = [
            { task_id: '1', title: 'Задача 1' },
            { task_id: '2', title: 'Задача 2' },
            { task_id: '3', title: 'Задача 3' },
        ];

        wrapper.setProps({ tasks });
        await wrapper.find('input').setValue('Задача 4');
        wrapper.vm.$nextTick(); 

        expect(wrapper.vm.filteredTasks).toEqual([]);
    });


})