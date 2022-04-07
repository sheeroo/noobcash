import axios from 'axios';

const getIP = () => {
    const ip = localStorage.getItem('ip');
    if (ip === null) {
        throw {
            message: 'Your are not logged in'
        }
    }
    return ip;
}

export const getBalance = async () => {
    try {
    const ip = getIP();
    const instance = axios.create({
        baseURL: `http://${ip}`,
        timeout: 5000
    });
       const { data } = await instance.get('/balance');
       return data;
    } catch (error) {
        console.error('Balance Error', error);
        throw error;
    }
}

export const newTransaction = async ({ receiver, amount }) => {
    const ip = getIP();
    const instance = axios.create({
        baseURL: `http://${ip}`,
        timeout: 5000
    });
    try {
        const { data } = await instance.post('/transaction/create', { receiver, amount });
        return data;
    } catch (error) {
        throw error.response;
    }
}

export const getRing = async () => {
    try {
        const ip = getIP();
        const instance = axios.create({
            baseURL: `http://${ip}`,
            timeout: 5000
        });
        const { data } = await instance.post('/state/get');
        const formattedArray = data?.ring?.map((item) => {
            return { address: item["public_key"], id: item.id, port: item.port };
        });
        return formattedArray;
    } catch (error) {
        console.error('Ring Error', error);
        throw error;
    }
}

export const transactionLog = async () => {
    try {
        // const ip = getIP();
        const instance = axios.create({
            baseURL: `http://192.168.0.96:5000`,
            timeout: 5000
        });
        const { data } = await instance.get('/transaction/view');
        return data;
    } catch (error) {
        console.error('Transction Log Error', error);
        throw error;
    }
}