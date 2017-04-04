using System;
using RBFG.Insurance.Framework.DataParsing.Base;


namespace RBFG.Insurance.YJT0.DataParsing
{

	public class ActivationStatusResponse : Segment
	{

		public ActivationStatusResponse()
		{
			Fields.Add("Label", new Field(FT.Alpha, 6, "@@ASRP"));
			Fields.Add("ActivationCode", new Field(FT.Alpha, 10));
			Fields.Add("ReturnCode", new Field(FT.Alpha, 3));
			Fields.Add("ActivationStatus", new Field(FT.Alpha, 1));
			Fields.Add("PolicyNumber", new Field(FT.Alpha, 11));

			Fields.Add("ExpiryDate", new Field(FT.DateTime, "yyyyMMdd", 8));
			Fields.Add("TransactionNumber", new Field(FT.Integer, 5));
			Fields.Add("EffectiveDate", new Field(FT.DateTime, "yyyyMMdd", 8));
			Fields.Add("EffectiveTime", new Field(FT.DateTime, "hhmmss", 6));
			Fields.Add("TransactionEffectiveDate", new Field(FT.DateTime, "yyyyMMdd", 8));

			Fields.Add("TransactionExpiryDate", new Field(FT.DateTime, "yyyyMMdd", 8));
			Fields.Add("LineofBusiness", new Field(FT.Alpha, 1));
			Fields.Add("AnnualDiscountedPremium", new Field(FT.Decimal72, 9)); // dec 2
			Fields.Add("PolicyStatus", new Field(FT.Alpha, 1));
			Fields.Add("PolicyHolder1LastName", new Field(FT.Alpha, 30));

			Fields.Add("PolicyHolder1FirstName", new Field(FT.Alpha, 30));
			Fields.Add("PolicyHolder2LastName", new Field(FT.Alpha, 30));
			Fields.Add("PolicyHolder2FirstName", new Field(FT.Alpha, 30));
			Fields.Add("DateofBirth", new Field(FT.DateTime, "yyyyMMdd", 8));
			Fields.Add("PlanCode", new Field(FT.Alpha, 8));

			Fields.Add("PolicyTerm", new Field(FT.Alpha, 3));
			Fields.Add("TransactionPremiumSign", new Field(FT.Alpha, 1));
			Fields.Add("TransactionPremium", new Field(FT.Decimal72, 9)); // dec 2
			Fields.Add("WrittenPremium", new Field(FT.Decimal72, 9));    // dec 2
			Fields.Add("THQuotePolicyNumber", new Field(FT.Alpha, 8));

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


		public string ActivationStatus
		{
			get
			{
				return Fields["ActivationStatus"].String;
			}
			set
			{
				Fields["ActivationStatus"].String = value;
			}
		}

/**/
		public string PolicyNumber
		{
			get
			{
				return Fields["PolicyNumber"].String;
			}
			set
			{
				Fields["PolicyNumber"].String = value;
			}
		}


		public DateTime ExpiryDate
		{
			get
			{
				return Fields["ExpiryDate"].DateTime;
			}
			set
			{
				Fields["ExpiryDate"].DateTime = value;
			}
		}

	
		public int TransactionNumber
		{
			get
			{
				return Fields["TransactionNumber"].Integer;
			}
			set
			{
				Fields["TransactionNumber"].Integer = value;
			}
		}


		public DateTime EffectiveDate
		{
			get
			{
				return Fields["EffectiveDate"].DateTime;
			}
			set
			{
				Fields["EffectiveDate"].DateTime = value;
			}
		}
	

		public DateTime EffectiveTime
		{
			get
			{
				return Fields["EffectiveTime"].DateTime;
			}
			set
			{
				Fields["EffectiveTime"].DateTime = value;
			}
		}


		public DateTime TransactionEffectiveDate
		{
			get
			{
				return Fields["TransactionEffectiveDate"].DateTime;
			}
			set
			{
				Fields["TransactionEffectiveDate"].DateTime = value;
			}
		}
	
		public DateTime TransactionExpiryDate
		{
			get
			{
				return Fields["TransactionExpiryDate"].DateTime;
			}
			set
			{
				Fields["TransactionExpiryDate"].DateTime = value;
			}
		}


		public string LineofBusiness
		{
			get
			{
				return Fields["LineofBusiness"].String;
			}
			set
			{
				Fields["LineofBusiness"].String = value;
			}
		}	


		public decimal AnnualDiscountedPremium
		{
			get
			{
				return Fields["AnnualDiscountedPremium"].Decimal;
			}
			set
			{
				Fields["AnnualDiscountedPremium"].Decimal = value;
			}
		}


		public string PolicyStatus
		{
			get
			{
				return Fields["PolicyStatus"].String;
			}
			set
			{
				Fields["PolicyStatus"].String = value;
			}
		}

	
		public string PolicyHolder1LastName
		{
			get
			{
				return Fields["PolicyHolder1LastName"].String;
			}
			set
			{
				Fields["PolicyHolder1LastName"].String = value;
			}
		}


		public string PolicyHolder1FirstName
		{
			get
			{
				return Fields["PolicyHolder1FirstName"].String;
			}
			set
			{
				Fields["PolicyHolder1FirstName"].String = value;
			}
		}
	

		public string PolicyHolder2LastName
		{
			get
			{
				return Fields["PolicyHolder2LastName"].String;
			}
			set
			{
				Fields["PolicyHolder2LastName"].String = value;
			}
		}


		public string PolicyHolder2FirstName
		{
			get
			{
				return Fields["PolicyHolder2FirstName"].String;
			}
			set
			{
				Fields["PolicyHolder2FirstName"].String = value;
			}
		}
	
		public DateTime DateofBirth
		{
			get
			{
				return Fields["DateofBirth"].DateTime;
			}
			set
			{
				Fields["DateofBirth"].DateTime = value;
			}
		}


		public string PlanCode
		{
			get
			{
				return Fields["PlanCode"].String;
			}
			set
			{
				Fields["PlanCode"].String = value;
			}
		}


		public string PolicyTerm
		{
			get
			{
				return Fields["PolicyTerm"].String;
			}
			set
			{
				Fields["PolicyTerm"].String = value;
			}
		}


		public string TransactionPremiumSign
		{
			get
			{
				return Fields["TransactionPremiumSign"].String;
			}
			set
			{
				Fields["TransactionPremiumSign"].String = value;
			}
		}

	
		public decimal TransactionPremium
		{
			get
			{
				return Fields["TransactionPremium"].Decimal;
			}
			set
			{
				Fields["TransactionPremium"].Decimal = value;
			}
		}


		public decimal WrittenPremium
		{
			get
			{
				return Fields["WrittenPremium"].Decimal;
			}
			set
			{
				Fields["WrittenPremium"].Decimal = value;
			}
		}
	

		public string THQuotePolicyNumber
		{
			get
			{
				return Fields["THQuotePolicyNumber"].String;
			}
			set
			{
				Fields["THQuotePolicyNumber"].String = value;
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
