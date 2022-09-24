import {
    List,
    ListItem,
    ListIcon,
    Center,
  } from '@chakra-ui/react';
import { GiTrophyCup, GiMedal } from "react-icons/gi"

  export default function Leaderboard({data}) {

    return (
      <Center py={6}>
            <List spacing={3} textAlign="center" w="100%">
                            {data && data.map((el, i) => 
                                i <= 2
                                ? <ListItem key={i} bgColor="white" p="10px" borderRadius="10px" boxShadow="3px 3px 1px 1px #002b5b" cursor="pointer"> <ListIcon as={i == 0 ? GiTrophyCup : GiMedal} color={i == 0 ? "gold" : i == 1 ? "silver" : "bronze"} />{el.name}</ListItem> 
                                : <ListItem key={i} bgColor="white" p="10px" borderRadius="10px" boxShadow="3px 3px 1px 1px #002b5b" cursor="pointer">{el.name}</ListItem> 
                            )}
            </List>
      </Center>
    );
  }