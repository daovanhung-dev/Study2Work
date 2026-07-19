import mysql from "mysql2/promise";
import { env } from "./env.js";

const getConnection = async () => {
  const connection = await mysql.createConnection(env.databaseUrl);
  console.log("Database connected!");
  return connection;
};

export default getConnection;
