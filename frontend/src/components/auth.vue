<template>
  <!-- ICONS -->
<svg id="svg-source" height="0" version="1.1"  xmlns="http://www.w3.org/2000/svg" 
xmlns:xlink="http://www.w3.org/1999/xlink" style="position: absolute">
 <g id="man-people-user" data-iconmelon="Streamline Icon Set:de32eb2621491c1a881a9fe846236da1">
    <g id="Expanded">
      <g>
        <g>
          <path  d="M16.028,20c-4.764,0-8.639-4.486-8.639-10s3.875-10,8.639-10c4.763,0,8.638,4.486,8.638,10
				S20.791,20,16.028,20z M16.028,1.333C12,1.333,8.722,5.221,8.722,10s3.277,8.667,7.306,8.667c4.029,0,7.306-3.888,7.306-8.667
				S20.057,1.333,16.028,1.333z"></path>
        </g>
      <g>
         <path  d="M31.988,32H0.012v-4.515c0-1.967,1.245-3.733,3.097-4.395l8.224-2.266v-2.77h1.333v3.785L3.51,24.361
				c-1.275,0.458-2.165,1.72-2.165,3.124v3.182h29.309v-3.182c0-1.404-0.889-2.666-2.213-3.139l-9.107-2.506v-3.758h1.332v2.742
				l8.178,2.251c1.9,0.677,3.145,2.442,3.145,4.409V32z"></path>
       </g>
       <g>
                    <path  d="M21.865,8.812c-0.045,0-0.09-0.001-0.137-0.003c-1.5-0.055-3.25-1.004-4.361-2.287
				C16.59,7.513,15.48,8.15,14.106,8.383c-2.403,0.413-5.152-0.51-5.988-1.321l0.928-0.957c0.403,0.391,2.69,1.329,4.836,0.964
				c1.332-0.226,2.292-0.911,2.854-2.034l0.558-1.114l0.617,1.082c0.738,1.292,2.508,2.425,3.867,2.475
				c0.604,0.016,1.033-0.165,1.307-0.571l1.105,0.745C23.686,8.403,22.863,8.812,21.865,8.812z"></path>
                  </g>
                </g>
              </g>
            </g>
            <g id="lock-locker" data-iconmelon="Streamline Icon Set:5d43c6f45cdbecfd5b8a12bc9e5dd33c">
              <g id="Expanded">
                <g>
                  <g>
                    <circle  cx="16" cy="20" r="1.333"></circle>
                  </g>
          <g>
              <path  d="M16,25.333c-0.369,0-0.667-0.298-0.667-0.666v-4C15.333,20.298,15.631,20,16,20s0.667,0.298,0.667,0.667
				v4C16.667,25.035,16.369,25.333,16,25.333z"></path>
          </g>
          <g>
            <path  d="M28,32H4V12h24V32z M5.333,30.667h21.333V13.333H5.333V30.667z"></path>
        </g>
        <g>
         <path  d="M24,12.667h-1.333V8c0-3.676-2.991-6.667-6.667-6.667c-3.676,0-6.667,2.99-6.667,6.667v4.667H8V8
				c0-4.412,3.588-8,8-8c4.411,0,8,3.588,8,8V12.667z"></path>
           </g>
        </g>
      </g>
   </g>
</svg>
<!-- ICONS -->
    <Navbar/>
  <body style=" background-color: #1a1f25;color: #d3d3d3;">
    <main >
        <div class="flex-container">
          <div class="">
          <Text/>
         </div>
        <div class="form-container m-5">
          <div class="clear"></div> 
          <form action="#" @submit.prevent="handleSubmit">
            <h2 class="text-center">{{ isLogin ? 'Авторизация' : 'Регистрация' }}</h2>
          <div class="">
           <label class="user" for="text">
              <svg viewBox="0 0 32 32">
                 <g filter="">
                   <use xlink:href="#man-people-user"></use>
                 </g>
               </svg>
             </label>
           <input  class="user-input" placeholder="логин" type="text" id="login" v-model="login" @input="validatelogin" required maxlength="10" />
           <div v-if="loginError" class="error-message">{{ loginError }}</div>
            </div>  
          <div class="">
              <label class="lock" for="password">
             <svg viewBox="0 0 32 32">
             <g filter="">
            <use xlink:href="#lock-locker"></use>
               </g>
             </svg>
              </label>
            <input type="password" placeholder="пароль" id="password" v-model="password" @input="validatePassword" required  maxlength="10"/>
            <div v-if="passwordError" class="error-message">{{ passwordError }}</div>
          </div>
             <button type="submit" class="btn btn-light w-100" :disabled="!formValid">{{ isLogin ? 'Войти' : 'Зарегистрироваться' }}</button>   
             <p class="text-center mt-2" @click="toggleForm" style="cursor: pointer;">
               {{ isLogin ? 'Нет аккаунта?' : 'Есть аккаунт? Войдите!' }}
             </p>
         </form>
         </div>
     </div>
    </main>
  </body>
</template>
  
<script lang="ts">
  import axios from 'axios';
  import Navbar from './navbar.vue';
  import Text from './text.vue';
  import { defineComponent } from 'vue';
  import Cookies from 'js-cookie';
  interface Users {
    login: string,
    password: string
  }
  interface ComponentData {
    isLogin: boolean;
    login: string;
    password: string;
    loginError: string | null;
    passwordError: string | null;
    formValid: boolean;
    // users: Users[];
    currentuser_id: number | null;
  }
  
  
  export default defineComponent({
    components: {
      Navbar,
      Text
    },
    data(): ComponentData {
      return {
        isLogin: true,
        login: '',
        password: '',
        loginError: null,
        passwordError: null,
        formValid: false,
        // users: JSON.parse(localStorage.getItem('users')) || [],
        // users: JSON.parse(localStorage.getItem('users') ?? '[]'),
        currentuser_id: null,
      };
    },
    methods: {
      beforeCreate() {
  const styleSheets = document.styleSheets;
  for (let i = styleSheets.length - 1; i >= 0; i--) {
    const cssRules = styleSheets[i].cssRules;
    for (let j = cssRules.length - 1; j >= 0; j--) {
      styleSheets[i].deleteRule(j);
    }
  }
},
    toggleForm(): void {
      this.isLogin = !this.isLogin;
      this.login = '';
      this.password = '';
    },
    async handleSubmit(): Promise<void> {
      if (this.isLogin) {
        try {
          const params = new URLSearchParams();
          params.append('username', this.login);
          params.append('password', this.password);
          const response = await axios.post('/api/users/login', params.toString(), {
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
            },
           });
          const token = response.data.access_token;
          // сохраняем токен в локальном хранилище или куках
          // localStorage.setItem('token', token);
          Cookies.set('users_access_token', token, { expires: 1 });
          console.log('Авторизация успешна');
          this.$router.push('/base');
        } 
        catch (error: any) {
          if (axios.isAxiosError(error)) {
          if (error.response && error.response.status === 401) {
            alert('Неверный логин или пароль');
          } else {
            alert('Произошла ошибка при авторизации. Попробуйте еще раз.');
          }
        } else {
          alert('Произошла ошибка при авторизации. Попробуйте еще раз.');
        }
        }
      }
      else {
      // Регистрация
        const newUser: Users = {
        login: this.login,
        password: this.password,
        };
        try {
          const response = await axios.post('/api/user/registration', newUser);
          console.log(response);
          alert('Регистрация успешна!');
          this.isLogin = true;
        } 
        catch (error: any) {
          if (axios.isAxiosError(error)) {
            if (error.response) {
              // с сервака ошибка бо юзер уже есть
              console.error(error.response.data);
              alert(error.response.data.detail);
            } else {
              console.error(error);
            alert('Произошла ошибка при регистрации. Попробуйте еще раз.');
            }
            } else {
              console.error(error);
              alert('Произошла ошибка при регистрации. Попробуйте еще раз.');
            }
        }
      }
  },
    checkAuth(): void {
         const user_id = localStorage.getItem('currentuser_id');
        if (user_id) {
    this.currentuser_id = parseInt(user_id, 10);
    this.$router.push('/base');
   } else {
     this.$router.push('/');
   }
    },
    validatelogin(): void {
  const login = this.login.trim();
  this.loginError = null;

  if (!this.isLogin && login === '') {
    this.loginError = 'Заполните!';
  } else if (this.isLogin && login === '') {
    this.loginError = 'Введите логин';
  } else if (!this.isLogin &&  login.length < 3) {
    this.loginError = 'Минимум 3 символа';
  } else if (!this.isLogin &&  /^\d+$/.test(login)) {
    this.loginError = 'Нельзя использовать только цифры';
  } else {
    this.loginError = null;
    this.formValid = true;
  }
},
validatePassword(): void {
  const password = this.password.trim();
  this.passwordError = null;

  if (!this.isLogin && password === '') {
    this.passwordError = 'Заполните!';
  } else if (this.isLogin && password === '') {
    this.passwordError = 'Введите пароль';
  } else if (!this.isLogin &&  password.length < 6) {
    this.passwordError = 'Минимум 6 символов';
  } else if (!this.isLogin &&  !/[A-Z]/.test(password)) {
    this.passwordError = 'Нужна хотя бы одна заглавная буква';
  } else if (!this.isLogin &&  !/[a-z]/.test(password)) {
    this.passwordError = 'Нужна хотя бы одна строчная буква';
  } else if (!this.isLogin &&  !/\d/.test(password)) {
    this.passwordError = 'Нужна хотя бы одна цифра';
  } else if (!this.isLogin &&  !/[!"№%:,.;()_+=$%^&*<>/?|`~"]/.test(password)) {
    this.passwordError = 'Нужен хотя бы один специальный символ';
  } else {
    this.passwordError = null;
    this.formValid = true;
  }
},
  },
  created() {
    this.checkAuth();
    console.log('Пользователь уже авторизован. currentuser_id:', this.currentuser_id);  
  },
  watch: {
    loginError(value: string | null): void {
      this.formValid = value === null && this.passwordError === null;
    },
    passwordError(value: string | null): void {
      this.formValid = value === null && this.loginError === null;
    },
  },
});
</script>
  <style scoped>
   
  .flex-container {
      display: -webkit-flex;
      display: flex;
      -webkit-flex-direction: row; 
      flex-direction: row;
      -webkit-justify-content: center; 
      justify-content: center;
      -webkit-align-items: center; 
      align-items: center;
      min-height: 80vh; 
  }
  .block{
    display: flex;
    align-items: center;
    justify-content:space-between;
  }

.button {
  float: right;
  color: #7f8084;
  border: 1px solid #22272d;
  padding: 7px 15px;
  border-radius: 3px;
  font-size: 0.8em;
  cursor: pointer;
}

.button:hover {
  color: #d3d3d3;
}

.lock {
  position: absolute;
  width: 35px;
  height: 35px;
  margin-top: 6px;
  padding: 4px;
  left: 5px;
}
.lock::after {
  content: "";
  width: 1px;
  height: 30px;
  position: absolute;
  background: #22272d;
  top: 0px;
  left: 100%;
}

.user {
  position: absolute;
  width: 35px;
  height: 35px;
  margin-top: 8px;
  padding: 4px;
  left: 5px;
}
.user::after {
  content: "";
  width: 1px;
  height: 30px;
  position: absolute;
  background: #22272d;
  top: 0px;
  left: 100%;
}

input {
  width: 100%;
  padding: 5px;
  height: 40px;
  border-radius: 3px;
  margin: 5px 0;
  outline: none;
}

input[type="text"]:focus, input[type="password"]:focus {
  border: 1px solid white;
  box-shadow: none;
}

.user-input:focus .user {
  background: white !important;
}

input[type="text"] {
  background: transparent;
  border: 2px solid #22272d;
  padding-left: 45px;
  color: #e6b333;
}

input[type="password"] {
  background: transparent;
  border: 2px solid #22272d;
  padding-left: 45px;
  color: #e6b333;
}

input[type="submit"] {
  background: #e6b333;
  border: none;
  color: white;
  text-align: center;
  font-size: 0.8em;
  cursor: pointer;
}

input[type="radio"] {
  display: none;
}

.radio-check {
  width: 50px;
  height: 20px;
  border: 1px solid #22272d;
  border-radius: 30px;
  margin-top: 10px;
  float: left;
  text-align: center;
  padding: 4px 0;
  color: #e6b333;
  font-size: 0.65em;
  position: relative;
}
.radio-check label {
  margin: 0 2px;
  cursor: pointer;
}
.radio-check .switch-selection {
  display: block;
  position: absolute;
  width: 11px;
  height: 11px;
  border-radius: 50%;
  background: #babbbd;
  margin-top: -11px;
  margin-left: 11px;
  -webkit-transition: 0.2s ease-out;
  transition: 0.2s ease-out;
}

.radio-yes:checked ~ .switch-selection {
  margin-left: 25px !important;
}

.check-label {
  font-size: 0.8em;
  color: #7f8084;
  margin-top: 10px;
  float: left;
  padding: 3px 0;
  margin-left: 10px;
}

.forgot-label {
  font-size: 0.8em;
  color: #7f8084;
  margin-top: 10px;
  float: right;
  padding: 3px 0;
  cursor: pointer;
}

  </style>