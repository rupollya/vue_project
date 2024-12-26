import { beforeEach, test, describe, expect, vi } from 'vitest';
import axios from 'axios';
import AuthReg from '@/components/AuthReg.vue';
import { mount } from '@vue/test-utils';

vi.mock('axios');

describe('AuthReg.vue', () => {

  beforeEach(() => {
    vi.resetAllMocks();
  });

  describe('handleSubmit()', () => {
    
    test('Успешная регистрация', async () => {

      const wrapper = mount(AuthReg);

      wrapper.vm.isLogin = false;
      const newUser = { login: 'ppp', password: '123qQ!' };
      wrapper.vm.login = newUser.login;
      wrapper.vm.password = newUser.password;

      await wrapper.vm.handleSubmit();

      expect(axios.post).toHaveBeenCalledWith('/api/user/registration', newUser);
      expect(wrapper.vm.isLogin).toBe(true);
    });

    test('Успешная авторизация', async () => {
      const wrapper = mount(AuthReg);

      wrapper.vm.isLogin = true;
      const newUser = { login: 'ppp', password: '123qQ!' };
      wrapper.vm.login = newUser.login;
      wrapper.vm.password = newUser.password;

      await wrapper.vm.handleSubmit();

      expect(axios.post).toHaveBeenCalledWith('/api/users/login', 'username=ppp&password=123qQ%21', {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });
      expect(wrapper.vm.isLogin).toBe(true);
    });

    test('Тест на ошибку авторизации', async () => {
      const wrapper = mount(AuthReg);

      wrapper.vm.isLogin = true;
      const newUser = { login: 'ppp', password: '!123qQ!' };
      wrapper.vm.login = newUser.login;
      wrapper.vm.password = newUser.password;
      
      const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => {});

      await wrapper.vm.handleSubmit();

      expect(axios.post).toHaveBeenCalledWith('/api/users/login', 'username=ppp&password=%21123qQ%21', {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });
      
      expect(alertSpy).toHaveBeenCalledWith('Произошла ошибка при авторизации. Попробуйте еще раз.');
      
    });

    test.todo('', async () => {

    });


  });
});