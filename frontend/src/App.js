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
      console.log(res);
      setCarPlate(res.data);
  
    } catch (error) {
      console.log(error);
    }
  }
  

  return (
    <div>
      <Form sendCarPlate={sendCarPlate}
      car={car}
      setCar={setCar}
      />
      <div>
        { carPlate.car_name ? ( 
          <div>
            <h1>CAR NAME: {carPlate.car_name}</h1>
            <h1>CAR PLATE: {carPlate.car_plate}</h1> 
          </div>
        ) : null }
      </div>
    </div>
  );
}

export default App;
