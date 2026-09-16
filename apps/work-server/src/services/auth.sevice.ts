import prisma from "../config/prisma.config.js";

export const handleLoginStudent = async (
  email: string,
  matkhau: string,
  callback: any
) => {
  console.log("login student");
  const user = await prisma.sinhVien.findUnique({ where: { email: email } });

  if (!user) {
    console.log("ko co tai khoan");
    return callback(null, false, { message: `Email: ${email} not found` });
  }

  //compare password
  if (user.matkhau != matkhau) {
    console.log("Sai mat khau");
    return callback(null, false, { message: "Invalid password" });
  }
  return callback(null, user);
};


//======================================================================
//auth business
export const handleLoginBusiness = async (
  email: string,
  matkhau: string,
  callback: any
) => {
  console.log("login student");
  const user = await prisma.doanhNghiep.findUnique({ where: { email: email } });

  if (!user) {
    return callback(null, false, { message: `Email: ${user} not found` });
  }

  //compare password
  if (user.matkhau != matkhau) {
    return callback(null, false, { message: "Invalid password" });
  }
  return callback(null, user);
};
