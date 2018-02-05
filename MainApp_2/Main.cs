using System;
using System.Diagnostics;
using System.IO;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;


namespace MainApp_2
{
    public partial class Main : Form
    {
        public DateTime IT = DateTime.Now;
        public string initialTimeString;
        public Main()
        {
            InitializeComponent();
            initialTimeString = IT.Year.ToString() + "_" +
                IT.Month.ToString() + "_" +
                IT.Day.ToString() + "_" +
                IT.Hour.ToString() + "_" +
                IT.Minute.ToString() + "_" +
                IT.Second.ToString();
        }

        private void btn_Choose_Click(object sender, EventArgs e)
        {
            Form ChooseForm = new Segment_Chooser.Main(initialTimeString);
            ChooseForm.Show();
        }

        /// <summary>
        /// Runs Python to create directory and save initial picture
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void btn_testRunningPython_Click(object sender, EventArgs e)
        {
            Form test = new PythonService(initialTimeString);
            test.Show();
        }

        
    }
}
