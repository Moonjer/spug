/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import {observable} from "mobx";
import http from 'libs/http';

class Store {
    @observable branches = [];
    @observable record = {};
    @observable idMap = {};
    @observable isFetching = false;
    @observable formVisible = false;
    @observable importVisible = false;

    @observable f_name;
    @observable f_zone;
    @observable f_host;

    fetchRecords = () => {
        this.isFetching = true;
        return http.get('/api/branch/')
            .then(({branches}) => {
                this.branches = branches;
            })
            .finally(() => this.isFetching = false)
    };

    showForm = (info = {}) => {
        this.formVisible = true;
        this.record = info
    }
}

export default new Store()
