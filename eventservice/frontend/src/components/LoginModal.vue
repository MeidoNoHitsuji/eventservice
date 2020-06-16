<template>
    <b-modal id="login_modal" centered>
        <template v-slot:modal-title>
            <template v-if="type=='reg'">
                Форма регистрации
            </template>
            <template v-else>
                Форма входа
            </template>
        </template>
        <template v-slot:default>
            <b-form ref="reg" v-if="type=='reg'">
                <b-form-group id="input-group-1" label="Электронная почта:" label-for="input-1" description="Мы никогда не передадим вашу электронную почту кому-либо еще.">
                    <b-form-input id="input-1" v-model="reg.email" type="email" :state="validationEmail" required placeholder="Введите email"></b-form-input>
                </b-form-group>
                <b-form-group id="input-group-2" label="Username:" label-for="input-2" description="Ваш username должен состоять минимум из 5 символов и состоять только из латинского алфавита, цифр и знака подчёркивания!">
                    <b-form-input id="input-2" v-model="reg.username" type="text" :state="validationUsername" required placeholder="Введите username"></b-form-input>
                </b-form-group>
                <b-form-group id="input-group-3" label="Пароль:" label-for="input-3" description="Ваш пароль должен состоять минимум из 8 символов!">
                    <b-form-input id="input-3" v-model="reg.password" type="password" :state="validationPassword" required placeholder="Введите пароль"></b-form-input>
                </b-form-group>
                Уже eсть аккаунт? <b-button size="sm" variant="success" @click="swapSignup">Войти!</b-button>
            </b-form>
            <b-form ref="log" v-else>
                <b-form-group id="input-group-4" label="Username:" label-for="input-4">
                    <b-form-input id="input-4" v-model="log.username" type="text" :state="validationUsername" required placeholder="Введите username"></b-form-input>
                </b-form-group>
                <b-form-group id="input-group-5" label="Пароль:" label-for="input-5">
                    <b-form-input id="input-5" v-model="log.password" type="password" :state="validationPassword" required placeholder="Введите пароль"></b-form-input>
                </b-form-group>
                Нет аккаунта? <b-button size="sm" variant="success" @click="swapRegistration">Регистрация!</b-button>
            </b-form>
        </template>
        <template v-slot:modal-footer>
            <template v-if="type=='reg'">
                <b-button variant="success" @click="registration">Зарегистрироваться</b-button>
            </template>
            <template v-else>
                <b-button variant="success" @click="signup">Войти</b-button>
            </template>
        </template>
    </b-modal>
</template>

<script>
/* eslint-disable */
    import {HTTP} from '../assets/js/common'
    export default {
        name: "login_modal",
        data (){
            return {
                type: "log",
                reg: {
                    email: '',
                    username: '',
                    password: ''
                },
                log: {
                    username: '',
                    password: ''
                }
            }
        },
        computed: {
            validationPassword: function () {
                return this[this.type].password.length >= 8
            },
            validationUsername: function () {
                return this[this.type].username.length > 4 && /^[a-zA-Z0-9_]+$/.test(this[this.type].username)
            },
            validationEmail: function () {
                return /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(this.reg.email)
            }
        },
        methods: {
            toast: function (title, body, variant) {
                this.$bvToast.toast(body, {
                    title: title,
                    toaster: 'b-toaster-bottom-left',
                    solid: true,
                    appendToast: true,
                    variant: variant,
                })
            },
            openModal: function (type) {
                this.type = type || "log"
                this.$bvModal.show("login_modal")
            },
            hideModel: function(){
                this.$bvModal.hide("login_modal")
            },
            swapSignup: function () {
                this.type = 'log'
            },
            swapRegistration: function () {
                this.type = 'reg'
            },
            registration: function () {
                if (!this.$refs.reg.checkValidity()) {
                    return
                }
                HTTP.post('/registration', {
                    email: this.reg.email,
                    username: this.reg.username,
                    password: this.reg.password
                })
                .then(response => {
                    let data = response.data
                    if (data.ok == 1) {
                        this.$parent.saveUser(data.data)
                        document.location.reload(true);
                    } else {
                        this.toast('Ошибка', data.error, 'danger')
                    }
                })
                .catch(error => {
                    this.toast('Серверная ошибка', error, 'danger')
                });
            },
            signup: function () {
                if (!this.$refs.log.checkValidity()) {
                    return
                }
                HTTP.post('/signup', {
                    username: this.log.username,
                    password: this.log.password
                })
                .then(response => {
                    let data = response.data
                    if (data.ok == 1) {
                        this.$parent.saveUser(data.data)
                        document.location.reload(true);
                    } else {
                        this.toast('Ошибка', data.error, 'danger')
                    }
                })
                .catch(error => {
                    this.toast('Серверная ошибка', error, 'danger')
                });
            }
        }
    }
</script>