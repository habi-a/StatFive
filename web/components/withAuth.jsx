import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import { useStore } from "../pages";
import Verification from "../pages/verification";

const withAuth = (WrappedComponent) => {
  return (props) => {
    const Router = useRouter();
    const [verified, setVerified] = useState("0");
    const token = useStore((state) => state.token)
    const verif = useStore((state) => state.verification)

    useEffect(() => {
      if (!token) {
        Router.replace("/");
        setVerified("0")
      } else if(verif === false && token) {
        setVerified("1")
      } else {
        setVerified("2")
      }
    }, [Router, token, verif]);

    if (verified === "2") {
      return <WrappedComponent {...props} />;
    } else if(verified === "1") {
      return <Verification />;
    } else {
        return null;
    }
  };
};

export default withAuth;