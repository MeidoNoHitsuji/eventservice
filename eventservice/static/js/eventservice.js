csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value

getHeaders = function() {
    return {
        headers: {
            "X-CSRFToken": csrf_token
        }
    }
}

var login_modal = new Vue({
    el: "#login_modal",
    delimiters: ["${", "}"],
    data: {
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
        openModal: function (type) {
            this.type = type || "log"
            this.$bvModal.show("login_modal")
        },
        swapSignup: function () {
            this.type = 'log'
        },
        swapRegistration: function () {
            this.type = 'reg'
        },
        toast(title, body, variant) {
            this.$bvToast.toast(body, {
                title: title,
                toaster: 'b-toaster-bottom-left',
                solid: true,
                appendToast: true,
                variant: variant,
            })
        },
        registration: function () {
            if (!this.$refs.reg.checkValidity()) {
                return
            }
            axios.post('/registration', {
                    email: this.reg.email,
                    username: this.reg.username,
                    password: this.reg.password
                })
                .then(response => {
                    data = response.data
                    if (data.ok == 1) {
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
            axios.post('/signup', {
                    username: this.log.username,
                    password: this.log.password
                })
                .then(response => {
                    data = response.data
                    if (data.ok == 1) {
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
})

var create_modal = new Vue({
    el: "#create_modal",
    delimiters: ["${", "}"],
    data: {
        type: "create",
        event_types: ["Другое", "Звонок", "Встреча"], //Надо бы получать это при инициализации данных с сервера, но ради этого делать отдельную ссылку как-то плохо..
        title: "",
        description: "",
        event_type: "",
        date: "",
        time: "",
        id: 0
    },
    computed: {
        date_appointed: {
            get: function(){
                return this.date+" "+this.time
            },
            set: function(val){
                let d = val.split(" ")
                this.date = d[0]
                this.time = d[1]
            }
        }
    },
    methods: {
        toast(title, body, variant) {
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
            if(selected){
                this.id = selected.id
                this.title = selected.title,
                this.description = selected.description,
                this.event_type = selected.event_type
                this.date_appointed = selected.date_appointed
            }
            this.$bvModal.show("create_modal")
        },
        hideModal: function(){
            this.$bvModal.hide("create_modal")
        },
        deleteEvent: function(){
            axios.post('/delete', {
                event_id: this.id,
            }, getHeaders())
            .then(response => {
                data = response.data
                if (data.ok == 1) {
                    let i = 0
                    let index = -1
                    tableevents.items.forEach(f=>{
                        if(f.id==this.id){
                            index = i
                        }else{
                            i++
                        }
                    })
                    if (index>-1) {
                        tableevents.items.splice(index, 1);
                        tableevents.updateTable()
                        this.hideModal()
                    }
                    this.toast("Успех", data.data, "success")
                } else {
                    this.toast('Ошибка', data.error, 'danger')
                }
            })
            .catch(error => {
                this.toast('Серверная ошибка', error, 'danger')
            });
        },
        updateEvent: function(){
            axios.post('/update', {
                event_id: this.id,
                title: this.title,
                description: this.description,
                event_type: this.event_type,
                date_appointed: this.date_appointed
            }, getHeaders())
            .then(response => {
                data = response.data
                if (data.ok == 1) {
                    let i = 0
                    let index = -1
                    tableevents.items.forEach(f=>{
                        if(f.id==this.id){
                            index = i
                        }else{
                            i++
                        }
                    })
                    if (index>-1) {
                        tableevents.items[index] = {
                            id: this.id,
                            title: this.title,
                            description: this.description,
                            event_type: this.event_type,
                            date_appointed: this.date_appointed
                        };
                        this.hideModal()
                        tableevents.updateTable()
                    }
                    this.toast("Успех", data.data, "success")
                } else {
                    this.toast('Ошибка', data.error, 'danger')
                }
            })
            .catch(error => {
                this.toast('Серверная ошибка', error, 'danger')
            });
        },
        createEvent: function(){
            if(this.title.length<5 || this.title.length>50){
                this.toast("Ошибка", "Заголовок не может быть длиной меньше 5 символов и больше 50!", "danger")
                return
            }
            if(this.event_type == ""){
                this.toast("Ошибка", "Вам необходимо выбрать тип события!!", "danger")
                return
            }
            axios.post('/create', {
                title: this.title,
                description: this.description,
                event_type: this.event_type,
                date_appointed: this.date_appointed
            }, getHeaders())
            .then(response => {
                data = response.data
                if (data.ok == 1) {
                    tableevents.items.push({
                        id: data.data.id,
                        title: data.data.title,
                        description: data.data.description,
                        event_type: data.data.event_type,
                        date_appointed: data.data.date_appointed.replace('T', ' ').replace('Z', '')
                    })
                    this.toast("Успех", "Новое событие успешно создано!", "success")
                } else {
                    this.toast('Ошибка', data.error, 'danger')
                }
            })
            .catch(error => {
                this.toast('Серверная ошибка', error, 'danger')
            });
        }
    },
    created: function(){
        let date = new Date()
        let year = date.getFullYear()
        let month = date.getMonth()+1
        let day = date.getDate()
        this.date = `${year}-${month}-${day}`
        let hours = date.getHours()
        let minutes = date.getMinutes()
        let seconds = date.getSeconds()
        this.time = `${hours}:${minutes}:${seconds}`
    }
})

var tableevents = new Vue({
    el: "#table-events",
    delimiters: ["${", "}"],
    data: {
        filter: "",
        transProps: {
            // Transition name
            name: 'flip-list'
        },
        items: [],
        fields: [{
                key: 'id',
                label: 'Идентификатор',
                sortable: true
            },
            {
                key: 'title',
                label: 'Заголовок',
                sortable: true
            },
            {
                key: 'description',
                label: 'Описание',
                sortable: true
            },
            {
                key: 'event_type',
                label: 'Тип',
                sortable: true
            },
            {
                key: 'date_appointed',
                label: 'Дата назначения',
                sortable: true
            }
        ]
    },
    methods: {
        updateTable: function(){
            this.$refs.table.refresh()
        },
        openModalCreate: function(){
            create_modal.openModal()
        },
        onRowSelected(items) {
            if(items.length>0){
                create_modal.openModal("edit", items[0])
            }
        },
    },
    created: function(){
        axios.post('/get_data', {}, getHeaders())
        .then(response => {
            data = response.data
            if (data.ok == 1) {
                data.data.forEach(d => {
                    this.items.push({
                        id: d.id,
                        title: d.title,
                        description: d.description,
                        event_type: d.event_type,
                        date_appointed: d.date_appointed.replace('T', ' ').replace('Z', '')
                    })
                });
            } else {
                this.toast('Ошибка', data.error, 'danger')
            }
        })
        .catch(error => {
            this.toast('Серверная ошибка', error, 'danger')
        });
    }
})

var eventservice = new Vue({
    el: "#eventservice",
    delimiters: ["${", "}"],
    data: {

    },
    methods: {
        openModal: function (type) {
            login_modal.openModal(type)
        }
    }
})