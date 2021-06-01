/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import {observable} from "mobx";
import http from 'libs/http';

class Store {
    @observable zones = [];
    @observable datacenters = [];
    @observable deviceVersions = [];
    @observable operatingSystems = [];
    @observable hostMachines = [];

    @observable records = [];
    @observable permRecords = [];
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
        return http.get('/api/host/')
            .then(({hosts, datacenters, zones, perms, device_versions, operating_systems, host_machines}) => {
                this.zones = zones;
                this.datacenters = datacenters;
                this.deviceVersions = device_versions;
                this.operatingSystems = operating_systems;
                this.hostMachines = host_machines

                this.records = hosts;
                this.permRecords = hosts.filter(item => perms.includes(item.id));
                for (let item of hosts) {
                    this.idMap[item.id] = item
                }
            })
            .finally(() => this.isFetching = false)
    };

    showForm = (info = {}) => {
        this.formVisible = true;
        this.record = info
    }
}

export default new Store()
