import './App.css';
import Form from './components/Form';
import axios from 'axios';
import { useState } from 'react';


const App = () => {
  const [carPlate, setCarPlate] = useState({});
  const api = axios.create({
    baseURL: 'http://localhost:8000/',
  });
  const sendCarPlate = async (e,carPlate) => {
    e.preventDefault();
    try {
      const res = await api.get(`cars/${carPlate}`);
      setCarPlate(res.data);
      console.log("Res", res);
    } catch (error) {
      console.log(error);
    }
  }

  return (
    <div>
      <Form sendCarPlate={sendCarPlate}/>
      <div>
        <h1>CAR ID: {carPlate.id}</h1>
        <h1>CAR NAME: {carPlate.car_name}</h1>
        <h1>CAR PLATE: {carPlate.car_plate}</h1>
      </div>
    </div>
  );
}

export default App;
