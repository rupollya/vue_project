import { describe, test, expect, afterEach, beforeEach } from 'vitest';
import { shallowMount, VueWrapper } from '@vue/test-utils';
import AuthReg from '@/components/AuthReg.vue';


describe('AuthReg.vue', () => {

    let wrapper: VueWrapper<any> | null = null;
    beforeEach(() => {
        wrapper = shallowMount(AuthReg, {});
    })

    afterEach(() => {
        if (wrapper) {
            wrapper.unmount();
        }
    })

    test('Тест на переключение между формой авторизации и регистрации', () => {

        if (!wrapper) {
            throw new Error('wrapper не инициализирован');
        }

        const toggleButton = wrapper.find('#backforth');
        toggleButton.trigger('click');  
        expect(wrapper.vm.isLogin).toBe(false);
    });

    test('Тест на переключение между формой авторизации и регистрации', () => {

        if (!wrapper) {
            throw new Error('wrapper не инициализирован');
        }

        const toggleButton = wrapper.find('#backforth');
        toggleButton.trigger('click');
        expect(wrapper.vm.isLogin).toBe(false);
    });


    test('Тест на валидацию логина при авторизации', () => {

        if (!wrapper) {
            throw new Error('wrapper не инициализирован');
        }

        const loginInput = wrapper.find('#login');
        loginInput.setValue('');
        expect(wrapper.vm.loginError).toBe('Введите логин');
    });

    test('Тест на валидацию логина при регистрации', () => {

        if (!wrapper) {
            throw new Error('wrapper не инициализирован');
        }

        const toggleButton = wrapper.find('#backforth');
        toggleButton.trigger('click');

        const loginInput = wrapper.find('#login');
        loginInput.setValue('');
        expect(wrapper.vm.loginError).toBe('Заполните поле!');
    });

    test('Тест на валидацию пароля при авторизации', () => {

        if (!wrapper) {
            throw new Error('wrapper не инициализирован');
        }

        const passwordInput = wrapper.find('#password');
        passwordInput.setValue('');
        expect(wrapper.vm.passwordError).toBe('Введите пароль');
    });

    test('Тест на валидацию пароля при регистрации', () => {

        if (!wrapper) {
            throw new Error('wrapper не инициализирован');
        }

        const toggleButton = wrapper.find('#backforth');
        toggleButton.trigger('click');

        const passwordInput = wrapper.find('#password');
        passwordInput.setValue('');
        expect(wrapper.vm.passwordError).toBe('Заполните поле!');
    });

    test('Тест на отправку формы регистрации', async () => {

        if (!wrapper) {
            throw new Error('wrapper не инициализирован');
        }
    
        const toggleButton = wrapper.find('#backforth');
        toggleButton.trigger('click');
    
        const loginInput = wrapper.find('#login');
        loginInput.setValue('testlogin');
    
        const passwordInput = wrapper.find('#password');
        passwordInput.setValue('testpassword');
    
        const submitButton = wrapper.find('#regauthbutton');
        await submitButton.trigger('submit');
        expect(wrapper.vm.isLogin).toBe(false);
    });
})