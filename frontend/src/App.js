import './App.css';
import Form from './components/Form';
import axios from 'axios';
import { useState } from 'react';


const App = () => {
  const [carPlate, setCarPlate] = useState([]);
  const [car, setCar] = useState('');
  const api = axios.create({
    baseURL: 'http://localhost:8000/',
  });
  const sendCarPlate = async (carPlate) => {
    try {

      const res = await api.get(`cars/${carPlate}`);
      localStorage.setItem('Car', res.data);
      console.log(res.data);
      setCarPlate(res.data);
  
    } catch (error) {
      console.log(error);
    }
  }
  

  return (
    <div>
      <Form sendCarPlate={(car, setCar, sendCarPlate)}/>
      <div>
        {carPlate.map((car, index) => (
          <div key={index}>
            <h1>{car.id}</h1>
            <h1>{car.car_name}</h1>
            <h1>{car.car_plate}</h1>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
