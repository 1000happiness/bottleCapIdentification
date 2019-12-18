import React, { Component } from "react";
import { Typography, Layout, Row, Col, Avatar, Button, Collapse, Table } from 'antd';

import "../src/main.css";

const { Header, Footer, Content } = Layout;
const { Text } = Typography;
const { Panel } = Collapse;

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
            labeledData: null
        }
    }

    componentDidMount() {
        this.setState({
            labeledData : [
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

    render() {
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
                                    <Button>
                                        选择文件
                                    </Button>
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
                                    <div id = "imageDiv">
                                        <Avatar
                                            id = "imageAvatar"
                                            src="https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png"
                                            shape="square"
                                            size={500}
                                        />
                                    </div>
                                </Col>
                                <Col id="outputImageCol" span={12}>
                                    <div id = "imageDiv">
                                        <Avatar
                                            id = "imageAvatar"
                                            src="https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png"
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
