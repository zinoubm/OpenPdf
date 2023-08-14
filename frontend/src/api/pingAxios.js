import axios from "./axios"

async function ping() {
    const res = await axios.get('http://localhost:8000/api/v1/users/sanity');
}

export default ping