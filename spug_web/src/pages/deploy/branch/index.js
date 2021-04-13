import React from 'react';
import { observer } from 'mobx-react';
import { Input, Button, Select } from 'antd';
import { SearchForm, AuthDiv, AuthCard } from 'components';
import ComTable from './Table';
import store from './store';

export default observer(function () {
    return (
        <AuthCard auth="branch.branch.view">
            <AuthDiv auth="branch.branch.add" style={{marginBottom: 16}}>
                <Button type="primary" icon="plus" onClick={() => store.showForm()}>新建</Button>
            </AuthDiv>
            <ComTable/>
        </AuthCard>
    )
})
