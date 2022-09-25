import { Flex, Box, Heading, List, ListItem, Input, Text, ListIcon, Button, Select } from '@chakra-ui/react'
import SimpleSidebar from "../components/Menu"
import { useEffect, useState } from 'react';
import withAuth from '../components/withAuth';
import { getAllUser } from '@mokhta_s/react-statfive-api';
import { RiAdminFill } from 'react-icons/ri';
import axios from 'axios';
import { API_URL } from '../static';
import AsyncStorage from '@react-native-async-storage/async-storage';

const Admin = () => {
    const [allUser, setAllUser] = useState([]);
    const [allComplexe, setAllComplexe] = useState([]);
    const [reload, setReload] = useState(0)
    const [name, setName] = useState('')
    const [phone, setPhone] = useState('')
    const [address, setAddress] = useState('')
    const [choice, setChoice] = useState(null)
    const [newComplex, setNewComplex] = useState(0)

    const getUser = async () => {
        const result = await getAllUser();
        if(choice?.id) {
            let user = result.data.data.find(o => o.id === choice.id);
            setChoice(user)
        }
        if(!result?.data.error) {
          setAllUser(result.data.data)
        }
    }

    const toAdmin = async (userId) => {
        const token = await AsyncStorage.getItem('token');
        await axios.get(API_URL + `/admin/make-admin/${userId}`, { headers:{"api-token": token} })
        setReload(reload + 1)
    }

    const getAllComplexe = async () => {
        const token = await AsyncStorage.getItem('token');
        const result = await axios.get(API_URL + `/admin/list-complex`, { headers:{"api-token": token} })
        if(!result?.data.error) {
            setAllComplexe(result.data.data)
        }
    }

    const createComplexe = async () => {
        const token = await AsyncStorage.getItem('token');
        await axios.post(API_URL + `/admin/create-complex`, {name, phone, address}, { headers:{"api-token": token} })
        setNewComplex(newComplex + 1)
    }

    const complexeToUser = async (id) => {
        let getId = id.split('/')
        const token = await AsyncStorage.getItem('token');
        await axios.get(API_URL + `/admin/user-to-complex/${getId[1]}/${getId[0]}`, { headers:{"api-token": token} })
        setReload(reload + 1)
    }

    const dissociateComplex = async (id) => {
        const token = await AsyncStorage.getItem('token');
        await axios.delete(API_URL + `/admin/user-dissociate-complex/${id}`, { headers:{"api-token": token} })
        setReload(reload + 1)
    }

    useEffect(() => {
        getAllComplexe()
    }, [newComplex])

    useEffect(() => {
        getUser()
    }, [reload])

  return (
    <Box>
        <SimpleSidebar />
        <Box pos="relative" left={{sm: "100px", md: "240px"}} w={{ md:"calc(100% -  240px)"}}>
            <Heading textAlign="center" mb="25px">Administration</Heading>
                <Flex flexDir="column" justifyContent="space-around" alignItems="center">
                    <Select w="25%" m="5px auto" placeholder='Choisir un utilisateur' onChange={(e) => e.target.value && setChoice(JSON.parse(e.target.value)) }>
                                {allUser && allUser.length > 0 ? 
                                allUser.map((el, i) => 
                                    <option key={i} value={JSON.stringify(el)}>{`${el.firstname} ${el.lastname}`}</option>
                                )
                            : <option value="null">Pas de complexe</option>
                        }
                    </Select>
                    {choice && 
                        <List spacing={3} textAlign="center" w="75%">
                        <ListItem bgColor="white" p="10px" mb="10px" borderRadius="10px" boxShadow="3px 3px 1px 1px #002b5b">
                            {`${choice.firstname} ${choice.lastname}`}
                            <ListIcon as={RiAdminFill} color={choice.role === 0 ? 'red.500' : 'green.500'} ml="20px" cursor="pointer" onClick={() => toAdmin(choice.id)} />
                            {choice.complex && <Text fontWeight="bold">Nom du complexe : {choice.complex.name}<br/> Adresse du complexe : {choice.complex.address}<br/> Numéro du complexe : {choice.complex.phone}</Text>}
                            <Select w="25%" m="5px auto" placeholder='Choisir un complexe' onChange={(e) => complexeToUser(e.target.value) }>
                                {allComplexe && allComplexe.length > 0 ? 
                                allComplexe.map((el, i) => 
                                    <option key={i} value={`${el.id}/${choice.id}`}>{el.name}</option>
                                )
                                : <option value="null">Pas de complexe</option>
                            }
                            </Select>
                            {choice.complex && <Button my="10px" width="50%" colorScheme="red" onClick={() => dissociateComplex(choice.id)}>Dissocier le complexe</Button>}
                        </ListItem> 
                    </List>  
                    }
                </Flex>
                <Flex ml="20px" mt="20px" background="white" border="2px solid #1C3879" borderRadius="5px" alignItems="center" justifyContent="center" flexDirection="column">
                        <Heading textAlign="center" mt="15px" mb="15px" size="md">Créer un complexe</Heading>
                        <Flex flexDir="column" w="75%">
                            <Input placeholder="Nom du complexe" mb="15px" value={name} onChange={(e) => setName(e.target.value)}/>
                            <Input placeholder="Numéro de téléphone" type="text" mb="30px" value={phone} onChange={(e) => setPhone(e.target.value)}/>
                            <Input placeholder="Adresse du complexe" type="text" mb="30px" value={address} onChange={(e) => setAddress(e.target.value)}/>
                            <Button my="10px" width="50%" colorScheme="green" disabled={name.length < 1 || phone.length < 1 || address.length < 1 ? true : false } onClick={() => createComplexe()}>Valider</Button>
                        </Flex>
                </Flex>
        </Box>
    </Box>
                            
  )
}

export default withAuth(Admin)