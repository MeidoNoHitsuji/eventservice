<template>
    <div id="table_events" class="mt-3 pl-2 pr-4">
        <b-row>
            <b-col>
                <b-input v-model="filter" type="search" id="filterInput" placeholder="Type to Search" class="w-auto"></b-input>
            </b-col>
            <b-col>
                <b-button class="ml-auto d-block" variant="info" @click="openModalCreate">Создать</b-button>
            </b-col>
        </b-row>
        <b-table ref="table" :items="items" :fields="fields" striped :filter="filter" selectable select-mode="single" @row-selected="onRowSelected" small primary-key="a" :tbody-transition-props="transProps" ></b-table>
    </div>
</template>

<script>
/* eslint-disable */
    import {HTTP} from '../assets/js/common'
    export default {
        name: "table_events",
        data () {
            return{
                filter: "",
                transProps: {
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
            updateTable: function(){
                this.$refs.table.refresh()
            },
            openModalCreate: function(){
                this.$parent.$refs.createmodal.openModal()
            },
            onRowSelected(items) {
                if(items.length>0){
                    this.$parent.$refs.createmodal.openModal("edit", items[0])
                }
            },
            updateData() {
                if(this.$parent.token == ""){
                    this.toast('Ошибка', "Сначала вы должны авторизоваться", 'danger')
                    return
                }
                HTTP.post('/get_data', {}, {
                    headers: {
                        Authorization: 'Token '+this.$parent.token
                    }
                })
                .then(response => {
                    let data = response.data
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
        },
        created: function(){
            this.updateData()
        }
    }
</script>