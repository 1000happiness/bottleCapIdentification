import React, { Component } from "react";
import { Typography, Layout, Row, Col, Avatar, Button, Collapse, Table, Upload, message } from 'antd';

import "../src/main.css";

const { Header, Footer, Content } = Layout;
const { Text } = Typography;
const { Panel } = Collapse;

var inputIndex = 2

const LabelerDatacolumns = [
    {
        title: '编号',
        dataIndex: 'id',
        key: 'id',
    },
    {
        title: '位置',
        dataIndex: 'location',//此处location转化成string表示
        key: 'location',
    },
    {
        title: '方向描述',
        dataIndex: 'directionDescription',
        key: 'directionDescription',
    },
    {
        title: '具体方向',
        dataIndex: 'direction',
        key: 'direction',
    }
]

class Mian extends Component {
    constructor(props) {
        super(props);
        this.state = {
            labeledData: null,
            inputImagePath: null,
            outputImagePath: null,
            i: 0,
        }
    }

    componentDidMount() {
        this.setState({
            labeledData: [
                {
                    id: 1,
                    location: "(5, 5)",
                    directionDescription: "向上",
                    direction: "(0,0,1)"
                },
                {
                    id: 1,
                    location: "(5, 5)",
                    directionDescription: "向上",
                    direction: "(0,0,1)"
                }
            ]
        })
    }

    componentWillUnmount() {
    }

    handleUpload(file) {
        const formData = new FormData();
        console.log(file)
        formData.append('image', file);

        var t = this;
        var response = null;
        var url = "http://localhost:8000/setImage";
        var response = fetch(url, {
            method: "POST",
            body: formData
        });
        console.log(response)
        this.setState({
            inputImagePath: "http://localhost:8000/getImage?image=" + inputIndex,
        })
        inputIndex = (inputIndex > 0 ? 0 : 2)
        
        // response.then(
        //     function (response) {
        //         console.log(response);
        //         if (response.status !== 200) {
        //             console.log("存在一个问题，状态码为：" + response.status);
        //             return;
        //         }
        //         return response.json();
        //     }
        // ).then(
        //     function (data) {
        //         if (data.success) {
        //             message.success("上传成功");
        //         }
        //         else {
        //             message.error("上传失败");
        //             console.log(data.errmsg);
        //         }
        //     }
        // ).catch(
        //     function (err) {
        //         message.error("上传失败");
        //         console.log(err);
        //     }
        // );
    };

    render() {

        var t = this;
        const props = {
            name: "file",
            beforeUpload: function (file) {
                const isJpgOrPng = file.type === 'image/jpeg' || file.type === 'image/png';
                if (!isJpgOrPng) {
                    message.error('你只能上传图片文件');
                    return false;
                }
                const isLt2M = file.size / 1024 / 1024 < 1;
                if (!isLt2M) {
                    message.error('图片大小不得大于1MB');
                    return false;
                }
                t.handleUpload(file);
                return false;
            },
            showUploadList: false,
        };


        return (
            <div id="mainDiv">
                <Layout id="mainLayot">
                    <Header
                        id="mainHeader"
                    >
                        <Text id="mainHeaderText">
                            瓶盖形态检测
                        </Text>
                    </Header>
                </Layout>
                <Layout
                    id="mainLayot"
                    style={{ minHeight: "100vh" }}
                >
                    <Layout id="mainLayot">
                        <Content id="mainContent">
                            <Row id="buttonRow">
                                <Col id="inputButtonCol" span={12}>
                                    <Upload {...props}>
                                        <Button>
                                            选择文件
                                        </Button>
                                    </Upload>
                                </Col>
                                <Col id="outputButtonCol" span={12}>
                                    <Button>
                                        获取结果
                                    </Button>
                                </Col>
                            </Row>
                            <Row id="discriptionRow">
                                <Col id="inputButtonCol" span={12}>
                                    <Text id="inputImageText">
                                        原图
                                    </Text>
                                </Col>
                                <Col id="outputButtonCol" span={12}>
                                    <Text id="outputImageText">
                                        处理后图片
                                    </Text>
                                </Col>
                            </Row>
                            <Row id="imageRow">
                                <Col id="inputImageCol" span={12}>
                                    <div id="imageDiv">
                                        <Avatar
                                            id="imageAvatar"
                                            src={this.state.inputImagePath}
                                            shape="square"
                                            size={500}
                                        />
                                    </div>
                                </Col>
                                <Col id="outputImageCol" span={12}>
                                    <div id="imageDiv">
                                        <Avatar
                                            id="imageAvatar"
                                            src={this.state.outputImagePath}
                                            shape="square"
                                            size={500}
                                        />
                                    </div>
                                </Col>
                            </Row>
                            <Row id="labeledDataRow">
                                <div id="labeledDataDiv">
                                    <Collapse
                                        id="labeledDataCollapse"
                                    >
                                        <Panel
                                            id="labeledDataPanel"
                                            header="标记信息"
                                            key="0"
                                        >
                                            <Table
                                                columns={LabelerDatacolumns}
                                                dataSource={this.state.labeledData}
                                            />
                                        </Panel>
                                    </Collapse>
                                </div>
                            </Row>
                        </Content>
                        <Footer id="mainFooter">
                            <Text id="mianFooterText">
                                Bottle Cap Identification ©2019
                            </Text>
                        </Footer>
                    </Layout>
                </Layout>
            </div>
        )
    }
}

export default Mian;
