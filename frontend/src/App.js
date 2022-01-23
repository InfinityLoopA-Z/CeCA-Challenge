import './App.css';
import Form from './components/Form';
import axios from 'axios';


const App = () => {
  const api = axios.create({
    baseURL: 'http://localhost:5000/api/',
  });
  const sendCarPlate = async (carPlate) => {
    try {
      const res = await api.post('/cars/', { carPlate });
      console.log(res.data);
    } catch (error) {
      console.log(error);
    }
  }
  return (
    <div>
      <Form sendCarPlate={sendCarPlate}/>
    </div>
  );
}

export default App;
