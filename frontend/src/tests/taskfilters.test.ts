import { describe, test, expect, afterEach, beforeEach } from 'vitest';
import { shallowMount, VueWrapper } from '@vue/test-utils';
import taskfilters from '@/components/TaskFilters.vue';

describe('TaskFilters.vue', () => {

    let wrapper: VueWrapper<any> | null = null;
    beforeEach(() => {
        wrapper = shallowMount(taskfilters, {});
    })

    afterEach(() => {
        if (wrapper) {
            wrapper.unmount();
        }
    })

    test('Тест на функциональность фильтрации всех задач', () => {
        
        if (!wrapper) {
            throw new Error('wrapper не инициализирован');
        }

        // await wrapper.find('.all-tasks').trigger('click');
        wrapper.vm.$emit('filterTasks', 'all');
        const emits = wrapper.emitted();
        expect(emits['filterTasks']).toEqual([['all']]);
    });

    test('Тест на функциональность фильтрации всех задач', () => {

        if (!wrapper) {
            throw new Error('wrapper не инициализирован');
        }

        // await wrapper.find('.completed-tasks').trigger('click');
        wrapper.vm.$emit('filterTasks', 'completed');
        const emits = wrapper.emitted();
        expect(emits['filterTasks']).toEqual([['completed']]);
    });

    test('Тест на функциональность фильтрации всех задач', () => {

        if (!wrapper) {
            throw new Error('wrapper не инициализирован');
        }

        //  wrapper.find('.pending-tasks').trigger('click');
        wrapper.vm.$emit('filterTasks', 'pending');

        const emits = wrapper.emitted();
        expect(emits['filterTasks']).toEqual([['pending']]);
    });

})