import mysql from "mysql2/promise";
import dotenv from "dotenv";
dotenv.config();

const getConnection = async () => {
  const connection = await mysql.createConnection(process.env.DATABASE_URL!);
  console.log("Database connected!");
  return connection;
};

export default getConnection;
