/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import React from 'react';
import {observer} from 'mobx-react';
import {Form, Input, message, Modal} from 'antd';
import http from 'libs/http';
import store from './store';

@observer
class ComForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            loading: false,
        }
    }

    handleSubmit = () => {
        this.setState({loading: true});
        const formData = this.props.form.getFieldsValue();
        formData['id'] = store.record.id;
        http.post('/api/app/', formData)
            .then(res => {
                message.success('操作成功');
                store.formVisible = false;
                store.fetchRecords()
            }, () => this.setState({loading: false}))
    };

    render() {
        const info = store.record;
        const {getFieldDecorator} = this.props.form;
        return (
            <Modal
                visible
                width={800}
                maskClosable={false}
                title={store.record.id ? '编辑应用' : '新建应用'}
                onCancel={() => store.formVisible = false}
                confirmLoading={this.state.loading}
                onOk={this.handleSubmit}>
                <Form labelCol={{span: 6}} wrapperCol={{span: 14}}>
                    <Form.Item required label="应用名称">
                        {getFieldDecorator('name', {initialValue: info['name']})(
                            <Input placeholder="请输入应用名称，例如：订单服务"/>
                        )}
                    </Form.Item>
                    <Form.Item required label="唯一标识符">
                        {getFieldDecorator('key', {initialValue: info['key']})(
                            <Input placeholder="请输入唯一标识符，例如：api_order"/>
                        )}
                    </Form.Item>
                    <Form.Item required label="git地址">
                        {getFieldDecorator('git_url', {initialValue: info['git_url']})(
                            <Input placeholder="请输入git仓库地址"/>
                        )}
                    </Form.Item>
                    <Form.Item label="备注信息">
                        {getFieldDecorator('desc', {initialValue: info['desc']})(
                            <Input.TextArea placeholder="请输入备注信息"/>
                        )}
                    </Form.Item>
                </Form>
            </Modal>
        )
    }
}

export default Form.create()(ComForm)
