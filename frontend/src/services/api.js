import axios from 'axios';
import { Platform } from 'react-native';


const getBaseURL = () => {
  if (Platform.OS === 'web') {
    return 'http://localhost:8000'; 
  }
  return 'http://192.168.1.130:8000'; 
};

const api = axios.create({
  baseURL: getBaseURL(),
});

export default api;