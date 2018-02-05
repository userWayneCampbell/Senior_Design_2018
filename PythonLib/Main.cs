using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace PythonLib
{
    public class Init
    {
        static public string filepathDate;
        public static void IntFilePathDate()
        {
            DateTime IT = DateTime.Now;
            filepathDate = IT.Year.ToString() + "_" +
                        IT.Month.ToString() + "_" +
                        IT.Day.ToString() + "_" +
                        IT.Hour.ToString() + "_" +
                        IT.Minute.ToString() + "_" +
                        IT.Second.ToString();
        }   
    }
}
