using System;
using System.Text;
using System.Collections;
using System.Collections.Specialized;
using RBFG.Insurance.Framework.DataParsing.Base;


namespace RBFG.Insurance.YJT0.DataParsing
{
	public class WQ222Header : Segment
	{
		
		public WQ222Header()
		{
			Fields.Add("RequestCode", new Field(FT.Alpha, 3, "222"));
			Fields.Add("WebUID", new Field(FT.Alpha, 32));
			Fields.Add("Date", new Field(FT.DateTime, "yyyyMMdd", 8));
			Fields.Add("Time", new Field(FT.DateTime, "hhmmss", 6));
			Fields.Add("ReturnCode", new Field(FT.Alpha, 3));
		}
		

		public string RequestCode
		{
			get
			{
				return Fields["RequestCode"].String;
			}
			set
			{
				Fields["RequestCode"].String = value;
			}
		}


		public string WebUID
		{
			get
			{
				return Fields["WebUID"].String;
			}
			set
			{
				Fields["WebUID"].String = value;
			}
		}


		public DateTime Date
		{
			get
			{
				return Fields["Date"].DateTime;
			}
			set
			{
				Fields["Date"].DateTime = value;
			}
		}


		public DateTime Time
		{
			get
			{
				return Fields["Time"].DateTime;
			}
			set
			{
				Fields["Time"].DateTime = value;
			}
		}


		public string ReturnCode
		{
			get
			{
				return Fields["ReturnCode"].String;
			}
			set
			{
				Fields["ReturnCode"].String = value;
			}
		}	
	}
}