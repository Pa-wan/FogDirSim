import React from 'react';
import { Table } from 'reactstrap';
import { URL } from "../costants"
import MyAppDevice from "./MyAppDevice"
import {BarChart} from 'react-easy-chart';
import Quadretti from "./Quadretti"

let alert_to_color = {
  "APP_HEALTH": "#CD533B",
  "DEVICE_REACHABILITY": "grey",
  "MYAPP_CPU_CONSUMING": "#E3B505",
  "MYAPP_MEM_CONSUMING": "#4392F1",
  "NO_ALERTS": "#33753e"
}
let compress_alert = {
  "APP_HEALTH": "HEALTH",
  "DEVICE_REACHABILITY": "DEVICE",
  "MYAPP_CPU_CONSUMING": "CPU",
  "MYAPP_MEM_CONSUMING": "MEM",
  "NO_ALERTS": "NO"
}

export default class MyAppsTable extends React.Component {
  constructor(props){
    super(props)
    this.state = {myapps: [], myappOnDevice: []}
  }

  getData = () => {
    fetch(URL+"/result/myapps")
      .then(res => res.json())
      .then(res => this.setState({myapps: res}))
    setTimeout(this.getData, 1000)
  }

  componentWillMount(){
    this.getData()
  }

  render() {
    return (
      <Table striped>
        <thead>
          <tr>
            <th scope="row">#</th>
            <th>MyApp ID</th>
            <th>Name</th>
            <th>Up Prob.</th>
            <th>Down Prob.</th>
            <th>Installed Probability</th>
            <th>Alerts</th>
          </tr>
        </thead>
        <tbody>
          {
            this.state.myapps.map((myapp, i) => {
              let pie_data = []
              for (let k in myapp.ALERT_PERCENTAGE){
                pie_data.push({x: k, y: myapp.ALERT_PERCENTAGE[k]*100, color: alert_to_color[k]})
              }
              return <tr key={myapp.myappId}>
              <td>{i}</td>
              <td>{myapp.myappId}</td>
              <td>{myapp.name}</td>
              <td>{(myapp.UP_PERCENTAGE * 100).toFixed(2)} %</td>
              <td>{(100 - (myapp.UP_PERCENTAGE * 100)).toFixed(2)} %</td>
              <td>{Object.keys(myapp.ON_DEVICE_PERCENTAGE)
                        .map(k => <MyAppDevice key={k} deviceId={k} time={myapp.ON_DEVICE_PERCENTAGE[k] * 100} startTime={myapp.ON_DEVICE_START_TIME[k]*100}/>)}
                </td>
              <td>
                <table className="quadretto">
                <tbody><tr>
                  <td>
                      <BarChart
                        axes
                        yDomainRange={[0, 100]}
                        axisLabels={{x: 'Alert Type', y: '%'}}
                        height={150}
                        width={400}
                        yTickNumber={3}
                        data={pie_data.map(e => ({x: compress_alert[e.x], y: e.y, color: e.color})) }
                      />
                  </td>
                  </tr><tr>
                  <td>
                  <Quadretti data={pie_data.map(val => { return {color: val.color, val: val.y, name: val.x}} )} />
                  </td>
                  </tr>
                </tbody>
                </table>
              </td>
            </tr>
            })
          }
        </tbody>
      </Table>
    );
  }
}