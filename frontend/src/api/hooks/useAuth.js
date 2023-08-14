import { useCookies } from "react-cookie";


function useAuth() {
    const [cookies, setCookie] = useCookies(["token"]);

    const getToken = () => {
        if (cookies.token === "null") {
            return null
        }

        return cookies.token
    }
    const setToken = (token) => {
        setCookie("token", token, { path: "/" });
    }
    const deleteToken = () => {
        setCookie("token", null, { path: "/" });
    }

    return {
        getToken,
        setToken,
        deleteToken,
    }
}

export default useAuth