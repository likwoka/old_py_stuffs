using System;
using RBFG.Insurance.Framework.DataParsing.Base;


namespace RBFG.Insurance.YJT0.DataParsing
{
	public class ActivationStatusRequest : Segment
	{
		public ActivationStatusRequest()
		{
			Fields.Add("Label", new Field(FT.Alpha, 6, "@@ASRQ"));
			Fields.Add("ActivationCode", new Field(FT.Alpha, 10));
			Fields.Add("EndSegment", new Field(FT.Alpha, 1, "|"));
		}


		public string Label
		{
			get
			{
				return Fields["Label"].String;
			}
			set
			{
				Fields["Label"].String = value;
			}
		}


		public string ActivationCode
		{
			get
			{
				return Fields["ActivationCode"].String;
			}
			set
			{
				Fields["ActivationCode"].String = value;
			}
		}


		public string EndSegment
		{
			get
			{
				return Fields["EndSegment"].String;
			}
			set
			{
				Fields["EndSegment"].String = value;
			}
		}
	}	
}