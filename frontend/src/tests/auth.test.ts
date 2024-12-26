import { describe, test, expect, afterEach, beforeEach } from 'vitest';
import { shallowMount, VueWrapper } from '@vue/test-utils';
import AuthReg from '@/components/AuthReg.vue';

 

// describe - функция, которая группирует связанные тесты, она принимает два аргумента: строку с названием группы тестов и функцию, в которой определяются сами тесты

// let wrapper: VueWrapper<any> | null = null; переменная wrapper хранит экземпляр компонента auth

//  VueWrapper<any> указывает на то, что это обертка для Vue-компонента, а null означает, что изначально она не инициализирована

//  beforeEach(() => { ... }) — это функция, которая выполняется перед каждым тестом в группе

//  Использование shallowMount позволяет монтировать компонент без его дочерних компонентов

//  afterEach(() => { ... }) — эта функция выполняется после каждого теста в группе
// если переменная wrapper не равна null, вызывается метод unmount(), который очищает ресурсы и удаляет компонент из DOM.

// термин "монтировать" (или "mount") относится к процессу создания экземпляра компонента и его добавления в виртуальный DOM. Это позволяет разработчикам взаимодействовать с компонентом так, как если бы он был частью реального приложения. 

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

    // положительные тесты

    // авторизация
    // тесты на валидацию отдельно для логина и пароля не требуются, так как валидация при регистрации в случае некорректных вводимых данных не прошла бы
    test('Тест на валидный логин и валидный пароль.', () => {

        if (!wrapper) {
            throw new Error('wrapper не инициализирован');
        };

        wrapper.setData({
            login: '12p',
            password: '123qQ!',
        });

        // проверяем валидацию логина
        wrapper.vm.validatelogin();
        expect(wrapper.vm.loginError).toBe(null);
        expect(wrapper.vm.formValid).toBe(true);

        // проверяем валидацию пароля
        wrapper.vm.validatePassword();
        expect(wrapper.vm.passwordError).toBe(null);
        expect(wrapper.vm.formValid).toBe(true);

    });

    // регистрация

        // тесты для логина

    test('Тест на валидный логин при использовании 3 симолов(не цифр).', () => {
        if (!wrapper) {
            throw new Error('wrapper не инициализирован');
        };

        wrapper.setData({
            login: 'pppp'
        });
        
        // проверяем валидацию логина
        wrapper.vm.validatelogin();
        expect(wrapper.vm.loginError).toBe(null);
        expect(wrapper.vm.formValid).toBe(true);

    });

    test('Тест на валидный логин при использовании цифр и иных символов.', () => {
        if (!wrapper) {
            throw new Error('wrapper не инициализирован');
        };

        wrapper.setData({
            login: '12!p'
        });
        
        // проверяем валидацию логина
        wrapper.vm.validatelogin();
        expect(wrapper.vm.loginError).toBe(null);
        expect(wrapper.vm.formValid).toBe(true);

    });

    test('Тест на валидный логин при минимальной длине(3 символа).', () => {

        if (!wrapper) {
            throw new Error('wrapper не инициализирован');
        };

        wrapper.setData({
            login: '1!p'
        });
        
        // проверяем валидацию логина
        wrapper.vm.validatelogin();
        expect(wrapper.vm.loginError).toBe(null);
        expect(wrapper.vm.formValid).toBe(true);

    });

    test('Тест на валидный логин при длине более минимальной.', () => {

        if (!wrapper) {
            throw new Error('wrapper не инициализирован');
        };

        wrapper.setData({
            login: '123wwww'
        });
        
        // проверяем валидацию логина
        wrapper.vm.validatelogin();
        expect(wrapper.vm.loginError).toBe(null);
        expect(wrapper.vm.formValid).toBe(true);

    });

        // тесты для пароля

            // очевидно, что вводимые данные будут корректны

    test('Тест на валидный пароль при минимальной длине(6 символов).', () => {

        if (!wrapper) {
            throw new Error('wrapper не инициализирован');
        };

        wrapper.setData({
            password: '123qQ!',
        });

        // проверяем валидацию пароля
        wrapper.vm.validatePassword();
        expect(wrapper.vm.passwordError).toBe(null);
        expect(wrapper.vm.formValid).toBe(true);

    })

    test('Тест на валидный пароль при длине более минимальной.', () => {

        if (!wrapper) {
            throw new Error('wrapper не инициализирован');
        };

        wrapper.setData({
            password: '123qQ!11',
        });

        // проверяем валидацию пароля
        wrapper.vm.validatePassword();
        expect(wrapper.vm.passwordError).toBe(null);
        expect(wrapper.vm.formValid).toBe(true);

    })
    
    // отрицательные тесты

        // Тесты для логина

            // авторизация

    test('Тест на пустой логин при авторизации.(Ошибка - заполните поле, появляется после стирания символа)', () => {
        
        if (!wrapper) {
            throw new Error('wrapper не инициализирован');
        }

        wrapper.setData({
            login: ''
        });

        wrapper.vm.validatelogin();
        expect(wrapper.vm.loginError).toBe('Введите логин'); 
        expect(wrapper.vm.formValid).toBe(false); 

    });

    test('Тест на логин, состоящий только из пробелов.(Ошибка - введите логин)', () => {
        
        if (!wrapper) {
            throw new Error('wrapper не инициализирован');
        }

        wrapper.setData({
            login: ' '
        });

        wrapper.vm.validatelogin();
        expect(wrapper.vm.loginError).toBe('Введите логин'); 
        expect(wrapper.vm.formValid).toBe(false); 

    })
            // регистрация

    test('Тест на пустой логин при регистрации.(Ошибка - заполните поле, появляется после стирания символа)', () => {
        
        if (!wrapper) {
            throw new Error('wrapper не инициализирован');
        }

        wrapper.setData({
            isLogin: false,
            login: ''
        });

        wrapper.vm.validatelogin();
        expect(wrapper.vm.loginError).toBe('Заполните поле!'); 
        expect(wrapper.vm.formValid).toBe(false);  

    }); 

    test('Тест на логин, состоящий только из пробелов.(Ошибка - заполните поле)', () => {

        if (!wrapper) {
            throw new Error('wrapper не инициализирован');
        }

        wrapper.setData({
            isLogin: false,
            login: ' '
        });

        wrapper.vm.validatelogin();
        expect(wrapper.vm.loginError).toBe('Заполните поле!'); 
        expect(wrapper.vm.formValid).toBe(false); 

    })

    test('Тест на логин меньше 3 символов(Ошибка - минимум 3 символа)', () => {
        
        if (!wrapper) {
            throw new Error('wrapper не инициализирован');
        }

        wrapper.setData({
            isLogin: false,
            login: '12'
        });

        wrapper.vm.validatelogin();
        expect(wrapper.vm.loginError).toBe('Минимум 3 символа'); 
        expect(wrapper.vm.formValid).toBe(false); 

    });

    test('Тест на логин состоящий только из цифр(Ошибка - нельзя использовать только цифры)', () => {
    
        if (!wrapper) {
            throw new Error('wrapper не инициализирован');
        }

        wrapper.setData({
            isLogin: false,
            login: '111'
        });

        wrapper.vm.validatelogin();
        expect(wrapper.vm.loginError).toBe('Нельзя использовать только цифры'); 
        expect(wrapper.vm.formValid).toBe(false); 

    });

        // Тесты для пароля

            // авторизация

    test('Тест на пустой пароль при авторизации.(Ошибка - введите пароль, появляется после стирания символа)', () => {
    
        if (!wrapper) {
            throw new Error('wrapper не инициализирован');
        }

        wrapper.setData({
            password: ''
        });

        wrapper.vm.validatePassword();
        expect(wrapper.vm.passwordError).toBe('Введите пароль'); 
        expect(wrapper.vm.formValid).toBe(false); 

    });

    test('Тест на пароль, состоящий только из пробелов.(Ошибка - введите пароль)', () => {

        if (!wrapper) {
            throw new Error('wrapper не инициализирован');
        }

        wrapper.setData({
            password: ' '
        });

        wrapper.vm.validatePassword();
        expect(wrapper.vm.passwordError).toBe('Введите пароль'); 
        expect(wrapper.vm.formValid).toBe(false);

    })

            // регистрация

    test('Тест на пустой пароль при регистрации.(Ошибка - заполните поле, появляется после стирания символа)', () => {
    
        if (!wrapper) {
            throw new Error('wrapper не инициализирован');
        }

        wrapper.setData({
            isLogin:false,
            password: ''
        });

        wrapper.vm.validatePassword();
        expect(wrapper.vm.passwordError).toBe('Заполните поле!'); 
        expect(wrapper.vm.formValid).toBe(false);

    });

    test('Тест на пароль, состоящий только из пробелов.(Ошибка - заполните поле)', () => {

        if (!wrapper) {
            throw new Error('wrapper не инициализирован');
        }

        wrapper.setData({
            isLogin:false,
            password: ' '
        });

        wrapper.vm.validatePassword();
        expect(wrapper.vm.passwordError).toBe('Заполните поле!'); 
        expect(wrapper.vm.formValid).toBe(false);
        
    })

    test('Тест на пароль меньше 6 символов.(Ошибка - минимум 6 символов)', () => {

        if (!wrapper) {
            throw new Error('wrapper не инициализирован');
        }

        wrapper.setData({
            isLogin:false,
            password: '123'
        });

        wrapper.vm.validatePassword();
        expect(wrapper.vm.passwordError).toBe('Минимум 6 символов'); 
        expect(wrapper.vm.formValid).toBe(false);

    })

    test('Тест на пароль без заглавной буквы.(Ошибка - нужна хотя бы одна заглавная буква)', () => {

        if (!wrapper) {
            throw new Error('wrapper не инициализирован');
        }

        wrapper.setData({
            isLogin:false,
            password: '123q!!'
        });

        wrapper.vm.validatePassword();
        expect(wrapper.vm.passwordError).toBe('Нужна хотя бы одна заглавная буква'); 
        expect(wrapper.vm.formValid).toBe(false);
        
    })

    test('Тест на пароль без строчной буквы.(Ошибка - нужна хотя бы одна строчная буква)', () => {

        if (!wrapper) {
            throw new Error('wrapper не инициализирован');
        }

        wrapper.setData({
            isLogin:false,
            password: '123Q!!'
        });

        wrapper.vm.validatePassword();
        expect(wrapper.vm.passwordError).toBe('Нужна хотя бы одна строчная буква'); 
        expect(wrapper.vm.formValid).toBe(false);

    })

    test('Тест на пароль без специального символа.(Ошибка - нужен хотя бы один специальный символ)', () => {

        if (!wrapper) {
            throw new Error('wrapper не инициализирован');
        }

        wrapper.setData({
            isLogin:false,
            password: '123QqQ'
        });

        wrapper.vm.validatePassword();
        expect(wrapper.vm.passwordError).toBe('Нужен хотя бы один специальный символ'); 
        expect(wrapper.vm.formValid).toBe(false);

    })

    test('Тест на пароль без цифр.(Ошибка - нужна хотя бы одна цифра)', () => {

        if (!wrapper) {
            throw new Error('wrapper не инициализирован');
        }

        wrapper.setData({
            isLogin:false,
            password: 'qqqQ!!'
        });

        wrapper.vm.validatePassword();
        expect(wrapper.vm.passwordError).toBe('Нужна хотя бы одна цифра'); 
        expect(wrapper.vm.formValid).toBe(false);

    })

})
