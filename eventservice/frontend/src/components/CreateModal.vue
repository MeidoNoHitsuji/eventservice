<template>
    <b-modal id="create_modal" centered>
        <template v-slot:modal-title>
            <template v-if="type=='create'">
                Форма создания нового событие!
            </template>
            <template v-else>
                Форма редактирования событие!
            </template>
        </template>
        <template v-slot:default>
            <b-form-group id="input-group-1" label="Заголовок:" label-for="input-1">
                <b-form-input id="input-1" v-model="title" type="text" required placeholder="Введите заголовок..."></b-form-input>
            </b-form-group>
            <b-form-group id="input-group-2" label="Описание:" label-for="input-2">
                <b-form-textarea id="input-2" v-model="description" max-rows="6" placeholder="Введите описание..."></b-form-textarea>
            </b-form-group>
            <b-form-group id="input-group-3" label="Тип:" label-for="input-3">
                <b-form-select v-model="event_type" id="input-3" :options="event_types">
                    <template v-slot:first>
                        <option value="">Выберите тип..</option>
                    </template>
                </b-form-select>
            </b-form-group>
            <b-form-group id="input-group-4" label="Дата назначения:">
                <b-input-group>
                    <b-form-datepicker v-model="date" placeholder="Выберите дату"></b-form-datepicker>
                    <b-form-timepicker v-model="time" show-seconds locale="ru" placeholder="Выберите время"></b-form-timepicker>
                </b-input-group>
            </b-form-group>
        </template>
        <template v-slot:modal-footer>
            <template v-if="type=='create'">
                <b-button variant="success" @click="createEvent">Создать</b-button>
            </template>
            <template v-else>
                <b-button variant="danger" @click="deleteEvent">Удалить</b-button>
                <b-button variant="success" @click="updateEvent">Обновить</b-button>
            </template>
        </template>
    </b-modal>
</template>

<script>
/* eslint-disable */
    import {HTTP} from '../assets/js/common'
    export default {
        name: "create_modal",
        data () {
            return{
                table_events: this.$parent.$refs.tableevents,
                type: "create",
                event_types: ["Другое", "Звонок", "Встреча"], //Надо бы получать это при инициализации данных с сервера, но ради этого делать отдельную ссылку как-то плохо..
                title: "",
                description: "",
                event_type: "",
                date: "",
                time: "",
                id: 0
            }
        },
        computed: {
            date_appointed: {
                get: function () {
                    return this.date + " " + this.time
                },
                set: function (val) {
                    let d = val.split(" ")
                    this.date = d[0]
                    this.time = d[1]
                }
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
            openModal: function (type, selected) {
                this.type = type || "create"
                if (selected) {
                    this.id = selected.id
                    this.title = selected.title,
                    this.description = selected.description,
                    this.event_type = selected.event_type
                    this.date_appointed = selected.date_appointed
                }
                this.$bvModal.show("create_modal")
            },
            hideModal: function () {
                this.$bvModal.hide("create_modal")
            },
            deleteEvent: function () {
                HTTP.delete(`/event/${this.id}/`, {
                    headers: {
                        Authorization: 'Token '+this.$parent.token
                    }
                })
                .then(response => {
                    let data = response.data
                    if (response.status == 204) {
                        let i = 0
                        let index = -1
                        this.table_events.items.forEach(f => {
                            if (f.id == this.id) {
                                index = i
                            } else {
                                i++
                            }
                        })
                        if (index > -1) {
                            this.table_events.items.splice(index, 1);
                            this.table_events.updateTable()
                            this.hideModal()
                        }
                        this.toast("Успех", "Событие успешно удалено", "success")
                    } else {
                        this.toast('Ошибка', "Неизвестная ошибка", 'danger')
                    }
                })
                .catch(error => {
                    this.toast('Серверная ошибка', error ? error : "Неизвестная ошибка", 'danger')
                });
            },
            updateEvent: function () {
                HTTP.put(`/event/${this.id}/`, {
                    title: this.title,
                    description: this.description,
                    event_type: this.event_type,
                    date_appointed: this.date_appointed
                }, {
                    headers: {
                        Authorization: 'Token '+this.$parent.token
                    }
                })
                .then(response => {
                    let data = response.data
                    if (response.status == 200) {
                        let i = 0
                        let index = -1
                        this.table_events.items.forEach(f => {
                            if (f.id == this.id) {
                                index = i
                            } else {
                                i++
                            }
                        })
                        if (index > -1) {
                            this.table_events.items[index] = {
                                id: this.id,
                                title: this.title,
                                description: this.description,
                                event_type: this.event_type,
                                date_appointed: this.date_appointed
                            };
                            this.hideModal()
                            this.table_events.updateTable()
                        }
                        this.toast("Успех", "Событие обновлено", "success")
                    } else {
                        this.toast('Ошибка', "Неизвестная ошибка", 'danger')
                    }
                })
                .catch(error => {
                    this.toast('Серверная ошибка', error ? error : "Неизвестная ошибка", 'danger')
                });
            },
            createEvent: function () {
                if (this.title.length < 5 || this.title.length > 50) {
                    this.toast("Ошибка", "Заголовок не может быть длиной меньше 5 символов и больше 50!", "danger")
                    return
                }
                if (this.event_type == "") {
                    this.toast("Ошибка", "Вам необходимо выбрать тип события!!", "danger")
                    return
                }
                HTTP.post('/event/', {
                    title: this.title,
                    description: this.description,
                    event_type: this.event_type,
                    date_appointed: this.date_appointed
                }, {
                    headers: {
                        Authorization: 'Token '+this.$parent.token
                    }
                })
                .then(response => {
                    let data = response.data
                    if (response.status == 201) {
                        this.table_events.items.push({
                            id: data.id,
                            title: data.title,
                            description: data.description,
                            event_type: data.event_type,
                            date_appointed: data.date_appointed.replace('T', ' ').replace('Z', '')
                        })
                        this.toast("Успех", "Новое событие успешно создано!", "success")
                    } else {
                        this.toast('Ошибка', data.error, 'danger')
                    }
                })
                .catch(error => {
                    this.toast('Серверная ошибка', error ? error : "Неизвестная ошибка", 'danger')
                });
            }
        },
        created: function () {
            let date = new Date()
            let year = date.getFullYear()
            let month = date.getMonth() + 1
            let day = date.getDate()
            this.date = `${year}-${month}-${day}`
            let hours = date.getHours()
            let minutes = date.getMinutes()
            let seconds = date.getSeconds()
            this.time = `${hours}:${minutes}:${seconds}`
        }
    }
</script>
