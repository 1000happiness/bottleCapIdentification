import React, { Component } from "react";
import { Typography, Layout, Row, Col, Button, Collapse, Table, Upload, message, Spin } from 'antd';

import "../src/main.css";

const { Header, Footer, Content } = Layout;
const { Text } = Typography;
const { Panel } = Collapse;

var inputIndex = 2
var outputIndex = 1

const labelerDatacolumns = [
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
            imgShape: [500,500],
            spin: false,
        }
    }

    componentDidMount() {
    }

    componentWillUnmount() {
    }

    handleUpload(file) {
        var formData = new FormData();
        formData.append('image', file);
        console.log(file)
        var t = this;
        var url = "http://localhost:8000/setImage";
        var response = fetch(url, {
            method: "POST",
            mode: "cors",
            body: formData
        });
        response.then(
            function(response){
                return response.json()
            }
        ).then(
            function(data){
                if(data.success){
                    t.setState({
                        inputImagePath: "http://localhost:8000/getImage?image=" + inputIndex,
                        outputImagePath: null,
                        imgShape: t.resize(data.imgWidth, data.imgHeight)
                    })
                    inputIndex = 2 + inputIndex
                }
                else{
                    message.error("获取图片失败")
                }
            }
        ).catch(
            function (err) {
                message.error("上传失败");
                console.log(err);
            }
        );
    };

    handleGetResult() {
        this.setState({
            spin: true,
        });
        
        var t = this;
        console.log(t);
        var url = "http://localhost:8000/getResultList";
        var response = fetch(url, {
            method: "GET",
            mode: "cors",
        });
        response.then(
            function(response){
                console.log(response)
                return response.json()
            }
        ).then(
            function(data){
                if(data.success){
                    t.setState({
                        labeledData: data.resultList,
                        spin: false,
                        outputImagePath: "http://localhost:8000/getImage?image=" + outputIndex
                    });
                    outputIndex = 2 + outputIndex;
                }
                else{
                    message.error("获取标记列表失败")
                }
            }
        ).catch(
            function (err) {
                message.error("获取标记列表失败");
                console.log(err);
            }
        );
    }

    resize(width, height) {
        var rate = 0;
        if(width > height){
            rate = width / 500;
        }
        else{
            rate = height / 500;
        }
        console.log([width / rate, height / rate])
        return [width / rate, height / rate]
    }

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
                const isLt2M = file.size / 1024 / 1024 < 6;
                if (!isLt2M) {
                    message.error('图片大小不得大于6MB');
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
                                    <Button onClick={() => this.handleGetResult()}>
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
                                        <img
                                            id="img"
                                            src={this.state.inputImagePath}
                                            width={this.state.imgShape[0]}
                                            height={this.state.imgShape[1]}
                                        />
                                    </div>
                                </Col>
                                <Col id="outputImageCol" span={12}>
                                    <div id="imageDiv">
                                        {
                                            this.state.spin ? 
                                            (
                                                <Spin id = "imgSpin" tip = "loading">
                                                </Spin>
                                            )
                                            :
                                            (
                                                <img
                                                    id="img"
                                                    src={this.state.outputImagePath}
                                                    width={this.state.imgShape[0]}
                                                    height={this.state.imgShape[1]}
                                                />
                                            )
                                        }
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
                                                columns={labelerDatacolumns}
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
